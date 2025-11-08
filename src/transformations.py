# src/transformations.py
import pandas as pd
import logging
import config as cfg

logger = logging.getLogger(__name__)


def clean_data(df_orders: pd.DataFrame, df_products: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """Limpia los dataframes, maneja nulos y convierte tipos."""
    logger.info("Iniciando limpieza de datos...")

    # Limpiar pedidos
    df_orders_cleaned = df_orders.dropna(
        subset=[cfg.COL_ORDER_ID, cfg.COL_CUSTOMER_ID, cfg.COL_PRODUCT_ID, cfg.COL_QUANTITY])
    df_orders_cleaned[cfg.COL_QUANTITY] = pd.to_numeric(df_orders_cleaned[cfg.COL_QUANTITY], errors='coerce')
    df_orders_cleaned[cfg.COL_ORDER_DATE] = pd.to_datetime(df_orders_cleaned[cfg.COL_ORDER_DATE], errors='coerce')

    # Limpiar productos
    df_products_cleaned = df_products.dropna(subset=[cfg.COL_PRODUCT_ID, cfg.COL_PRICE])
    df_products_cleaned[cfg.COL_PRICE] = pd.to_numeric(df_products_cleaned[cfg.COL_PRICE], errors='coerce')

    # Eliminar filas con valores nulos después de la coerción
    df_orders_cleaned = df_orders_cleaned.dropna()
    df_products_cleaned = df_products_cleaned.dropna()

    logger.info(
        f"Limpieza finalizada. Pedidos válidos: {len(df_orders_cleaned)}, Productos válidos: {len(df_products_cleaned)}")
    return df_orders_cleaned, df_products_cleaned


def enrich_orders(df_orders: pd.DataFrame, df_products: pd.DataFrame, df_customers: pd.DataFrame) -> pd.DataFrame:
    """Combina los dataframes y calcula nuevas columnas."""
    logger.info("Iniciando enriquecimiento de datos (merges)...")

    # Merge Pedidos y Productos para obtener el precio
    df_enriched = pd.merge(df_orders, df_products, on=cfg.COL_PRODUCT_ID, how="left")

    # Merge con Clientes para obtener sus datos (ej. "ciudad", "nombre")
    df_enriched = pd.merge(df_enriched, df_customers, on=cfg.COL_CUSTOMER_ID, how="left")

    # Calcular nueva columna
    df_enriched[cfg.COL_TOTAL_PRICE] = df_enriched[cfg.COL_QUANTITY] * df_enriched[cfg.COL_PRICE]

    # Manejar casos donde el producto no se encontró en el merge
    missing_price = df_enriched[cfg.COL_TOTAL_PRICE].isnull().sum()
    if missing_price > 0:
        logger.warning(f"Se encontraron {missing_price} pedidos sin un producto correspondiente. Se eliminarán.")
        df_enriched = df_enriched.dropna(subset=[cfg.COL_TOTAL_PRICE])

    logger.info(f"Enriquecimiento finalizado. Total de filas enriquecidas: {len(df_enriched)}")
    return df_enriched


def create_sales_summary(df_enriched: pd.DataFrame) -> pd.DataFrame:
    """Crea un reporte agregado de ventas por mes."""
    logger.info("Creando reporte 'Resumen de Ventas'...")

    if df_enriched.empty:
        logger.warning("No hay datos enriquecidos para crear el resumen de ventas.")
        return pd.DataFrame()

    df_enriched['sales_month'] = df_enriched[cfg.COL_ORDER_DATE].dt.to_period('M')

    df_summary = df_enriched.groupby('sales_month').agg(
        total_ventas=(cfg.COL_TOTAL_PRICE, 'sum'),
        pedidos_unicos=(cfg.COL_ORDER_ID, 'nunique'),
        productos_vendidos=(cfg.COL_QUANTITY, 'sum')
    ).reset_index()

    df_summary.sort_values(by='sales_month', ascending=False, inplace=True)
    logger.info("Reporte 'Resumen de Ventas' creado con éxito.")
    return df_summary


def create_top_products_report(df_enriched: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Crea un reporte de top N productos por ingresos."""
    logger.info(f"Creando reporte 'Top {top_n} Productos'...")

    if df_enriched.empty:
        logger.warning("No hay datos enriquecidos para crear el top de productos.")
        return pd.DataFrame()

    # Asumiendo que 'product_name' viene de df_products
    if 'product_name' not in df_enriched.columns:
        logger.warning("Columna 'product_name' no encontrada. Usando 'product_id' en su lugar.")
        group_col = cfg.COL_PRODUCT_ID
    else:
        group_col = 'product_name'

    df_top_products = df_enriched.groupby(group_col).agg(
        ingresos_totales=(cfg.COL_TOTAL_PRICE, 'sum'),
        unidades_vendidas=(cfg.COL_QUANTITY, 'sum')
    ).reset_index()

    df_top_products.sort_values(by='ingresos_totales', ascending=False, inplace=True)

    logger.info(f"Reporte 'Top {top_n} Productos' creado con éxito.")
    return df_top_products.head(top_n)