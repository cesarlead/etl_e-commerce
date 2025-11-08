# src/config.py
from pathlib import Path

# --- Rutas Base ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# --- Archivos de Entrada ---
FILE_ORDERS = DATA_DIR / "orders.csv"
FILE_CUSTOMERS = DATA_DIR / "customers.csv"
FILE_PRODUCTS = DATA_DIR / "products.csv"

# --- Archivo de Salida ---
FINAL_REPORT_FILE = OUTPUT_DIR / "sales_report.xlsx"

# --- Constantes del Reporte ---
SHEET_SALES_SUMMARY = "Resumen de Ventas"
SHEET_TOP_PRODUCTS = "Top Productos"

# --- Definición de Columnas (Buena práctica) ---
# Orders
COL_ORDER_ID = "order_id"
COL_CUSTOMER_ID = "customer_id"
COL_PRODUCT_ID = "product_id"
COL_QUANTITY = "quantity"
COL_ORDER_DATE = "order_date"

# Products
COL_PRICE = "price"

# Nuevas
COL_TOTAL_PRICE = "total_price"