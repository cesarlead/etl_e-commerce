# src/report_generator.py
import pandas as pd
from typing import Dict
import logging

logger = logging.getLogger(__name__)


def save_reports_to_excel(reports: Dict[str, pd.DataFrame], output_path: str):
    """
    Guarda múltiples dataframes en un solo archivo Excel, cada uno en una pestaña.
    """
    logger.info(f"Iniciando guardado de reporte en: {output_path}")

    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in reports.items():
                if df.empty:
                    logger.warning(f"No se guardará la pestaña '{sheet_name}' porque no contiene datos.")
                    continue

                df.to_excel(writer, sheet_name=sheet_name, index=False)
                logger.debug(f"Pestaña '{sheet_name}' agregada al reporte.")

        logger.info(f"Reporte guardado exitosamente en: {output_path}")

    except PermissionError:
        logger.error(f"Error de permisos. ¿Está el archivo '{output_path}' abierto?")
    except Exception as e:
        logger.exception(f"Error inesperado al guardar el archivo Excel: {e}")