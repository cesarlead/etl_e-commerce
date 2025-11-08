# src/data_loader.py
import pandas as pd
import logging
from typing import Dict, Optional

# Obtenemos el logger para este módulo
logger = logging.getLogger(__name__)


def load_csv(file_path: str, required_cols: Optional[list] = None) -> Optional[pd.DataFrame]:
    """
    Carga un archivo CSV de forma segura, con logging y validación de columnas.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Archivo cargado exitosamente: {file_path.name} ({len(df)} filas)")

        if required_cols:
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                logger.error(f"Faltan columnas en {file_path.name}: {missing_cols}")
                return None

        return df

    except FileNotFoundError:
        logger.critical(f"Archivo no encontrado: {file_path}")
        return None
    except pd.errors.ParserError:
        logger.error(f"Error al parsear el archivo CSV: {file_path}")
        return None
    except Exception as e:
        logger.exception(f"Error inesperado al cargar {file_path.name}: {e}")
        return None


def load_all_data(config) -> Dict[str, pd.DataFrame]:
    """
    Orquesta la carga de todos los archivos de datos fuente.
    """
    logger.info("Iniciando carga de datos fuente...")

    df_orders = load_csv(config.FILE_ORDERS,
                         [config.COL_ORDER_ID, config.COL_CUSTOMER_ID, config.COL_PRODUCT_ID, config.COL_QUANTITY])
    df_customers = load_csv(config.FILE_CUSTOMERS, [config.COL_CUSTOMER_ID])
    df_products = load_csv(config.FILE_PRODUCTS, [config.COL_PRODUCT_ID, config.COL_PRICE])

    dataframes = {
        "orders": df_orders,
        "customers": df_customers,
        "products": df_products
    }

    if any(df is None for df in dataframes.values()):
        logger.critical("Fallo en la carga de uno o más archivos. Abortando pipeline.")
        raise RuntimeError("No se pudieron cargar los datos fuente esenciales.")

    return dataframes