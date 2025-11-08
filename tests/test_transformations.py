# tests/test_transformations.py
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
from src import transformations as tf
from src import config as cfg


# Usamos pytest fixtures para crear datos de prueba reusables
@pytest.fixture
def sample_data():
    """Datos de prueba para las transformaciones."""
    orders = pd.DataFrame({
        cfg.COL_ORDER_ID: [1, 2, 3],
        cfg.COL_CUSTOMER_ID: ['A', 'B', 'A'],
        cfg.COL_PRODUCT_ID: [101, 102, 101],
        cfg.COL_QUANTITY: [2, 1, 3],
        cfg.COL_ORDER_DATE: ['2025-01-01', '2025-01-02', '2025-01-03']
    })

    products = pd.DataFrame({
        cfg.COL_PRODUCT_ID: [101, 102, 103],
        cfg.COL_PRICE: [10.0, 50.0, 100.0],
        'product_name': ['Producto A', 'Producto B', 'Producto C']
    })

    customers = pd.DataFrame({
        cfg.COL_CUSTOMER_ID: ['A', 'B', 'C'],
        'city': ['Ciudad X', 'Ciudad Y', 'Ciudad Z']
    })

    return {"orders": orders, "products": products, "customers": customers}


def test_clean_data_types(sample_data):
    """Prueba que los tipos de datos se convierten correctamente."""
    df_orders_clean, df_products_clean = tf.clean_data(sample_data['orders'], sample_data['products'])

    assert pd.api.types.is_datetime64_any_dtype(df_orders_clean[cfg.COL_ORDER_DATE])
    assert pd.api.types.is_numeric_dtype(df_orders_clean[cfg.COL_QUANTITY])
    assert pd.api.types.is_numeric_dtype(df_products_clean[cfg.COL_PRICE])


def test_enrich_orders_calculates_total_price(sample_data):
    """Prueba que el cálculo de TotalPrice es correcto."""
    df_orders_clean, df_products_clean = tf.clean_data(sample_data['orders'], sample_data['products'])
    df_enriched = tf.enrich_orders(df_orders_clean, df_products_clean, sample_data['customers'])

    # Valores esperados: [2*10.0, 1*50.0, 3*10.0] = [20.0, 50.0, 30.0]
    expected_totals = pd.Series([20.0, 50.0, 30.0], name=cfg.COL_TOTAL_PRICE)

    pd.testing.assert_series_equal(df_enriched[cfg.COL_TOTAL_PRICE], expected_totals, check_dtype=False)


def test_enrich_orders_handles_missing_product(sample_data):
    """Prueba que se eliminan pedidos con productos que no existen."""
    # Añadir un pedido con un producto inválido (104)
    sample_data['orders'].loc[len(sample_data['orders'])] = [4, 'C', 104, 1, '2025-01-04']

    df_orders_clean, df_products_clean = tf.clean_data(sample_data['orders'], sample_data['products'])
    df_enriched = tf.enrich_orders(df_orders_clean, df_products_clean, sample_data['customers'])

    # El pedido 4 debe ser eliminado durante el enriquecimiento
    assert len(df_enriched) == 3
    assert 4 not in df_enriched[cfg.COL_ORDER_ID].values


def test_create_top_products_report(sample_data):
    """Prueba que el reporte de top productos es correcto."""
    df_orders_clean, df_products_clean = tf.clean_data(sample_data['orders'], sample_data['products'])
    df_enriched = tf.enrich_orders(df_orders_clean, df_products_clean, sample_data['customers'])

    df_top = tf.create_top_products_report(df_enriched, top_n=2)

    assert len(df_top) == 2
    # Producto A: 20.0 + 30.0 = 50.0
    # Producto B: 50.0
    # El orden puede variar si hay empate, pero Producto A debe estar
    assert 'Producto A' in df_top['product_name'].values
    assert 'Producto B' in df_top['product_name'].values

    # Verificamos que el primero (el top 1) tiene los ingresos correctos
    # En este caso, puede ser A o B. Verifiquemos el total de A.
    total_a = df_top[df_top['product_name'] == 'Producto A']['ingresos_totales'].iloc[0]
    assert total_a == 50.0