# src/main.py
import logging
import config as cfg
from logging_config import setup_logging
from data_loader import load_all_data
import transformations as tf
from report_generator import save_reports_to_excel

# 1. Configurar el logging ANTES que nada
setup_logging()

# 2. Obtener el logger para el script principal
logger = logging.getLogger(__name__)


def main_pipeline():
    """
    Ejecuta el pipeline ETL completo.
    """
    logger.info("--- INICIANDO PIPELINE ETL E-COMMERCE ---")

    try:
        # 1. EXTRACT (Extraer)
        data = load_all_data(cfg)

        # 2. TRANSFORM (Transformar)
        logger.info("Iniciando fase de Transformación...")
        df_orders_clean, df_products_clean = tf.clean_data(data["orders"], data["products"])

        df_enriched = tf.enrich_orders(df_orders_clean, df_products_clean, data["customers"])

        # Generar los reportes finales
        df_sales_summary = tf.create_sales_summary(df_enriched)
        df_top_products = tf.create_top_products_report(df_enriched)

        logger.info("Fase de Transformación completada.")

        # 3. LOAD (Cargar)
        reports_to_save = {
            cfg.SHEET_SALES_SUMMARY: df_sales_summary,
            cfg.SHEET_TOP_PRODUCTS: df_top_products
        }

        cfg.OUTPUT_DIR.mkdir(exist_ok=True)  # Asegurar que el directorio de salida exista
        save_reports_to_excel(reports_to_save, cfg.FINAL_REPORT_FILE)

        logger.info("--- PIPELINE ETL COMPLETADO EXITOSAMENTE ---")

    except RuntimeError as e:
        logger.critical(f"Pipeline detenido por error en la carga de datos. {e}")
    except Exception as e:
        logger.exception(f"Error no controlado en el pipeline principal. {e}")
        logger.critical("--- PIPELINE FALLIDO ---")


if __name__ == "__main__":
    main_pipeline()