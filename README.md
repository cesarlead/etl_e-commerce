# Pipeline ETL de Análisis de Ventas E-commerce

Este proyecto es un pipeline de ETL (Extract, Transform, Load) construido en Python, diseñado para procesar datos de ventas de un e-commerce y generar reportes analíticos.

El propósito principal de este repositorio es demostrar las mejores prácticas en la construcción de pipelines de datos, incluyendo una estructura de proyecto modular, logging profesional, separación de responsabilidades (SRP) y pruebas unitarias (Unit Testing).

## Características Principales

* **Extracción (Extract):** Carga datos desde archivos CSV (`pedidos`, `clientes`, `productos`).
* **Transformación (Transform):**
    * Limpia y valida los datos (manejo de nulos, conversión de tipos).
    * Enriquece los datos cruzando información de las diferentes fuentes.
    * Calcula métricas clave (ej. `precio_total`).
    * Agrega datos para crear reportes (resumen mensual, top productos).
* **Carga (Load):** Guarda los reportes generados en un único archivo Excel con múltiples pestañas.
* **Logging Profesional:** Utiliza el módulo `logging` de Python para registrar eventos del pipeline tanto en consola (nivel INFO) como en un archivo rotativo (`logs/etl_process.log` - nivel DEBUG).
* **Pruebas Unitarias:** Incluye un conjunto de pruebas con `pytest` para verificar la lógica de transformación de forma aislada.

## Cómo Empezar

Sigue estos pasos para ejecutar el pipeline en tu máquina local.

### 1. Prerrequisitos

* Python 3.8 o superior
* Git

### 2. Instalación

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/TU_USUARIO/python_etl_ecommerce.git](https://github.com/TU_USUARIO/python_etl_ecommerce.git)
    cd python_etl_ecommerce
    ```

2.  (Recomendado) Crea un entorno virtual:
    ```bash
    # En Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Preparación de Datos

Coloca tus archivos de datos fuente en el directorio `/data`:

* `data/orders.csv`
* `data/customers.csv`
* `data/products.csv`

(Puedes incluir datos de *ejemplo* anónimos y pequeños en tu repositorio para que la gente pueda probarlo).

### 4. Ejecutar el Pipeline

Para ejecutar el proceso ETL completo, corre el script `main.py`:

```bash
python src/main.py
```

Si todo funciona correctamente, verás los logs en tu consola y el reporte final aparecerá en `output/sales_report.xlsx`. Un log detallado estará disponible en `logs/etl_process.log`.

## Cómo Ejecutar las Pruebas

Este proyecto usa `pytest` para las pruebas unitarias. Para verificar que toda la lógica de negocio funciona como se espera, simplemente ejecuta:

```bash
pytest
```

Verás una salida en la consola indicando si todas las pruebas pasaron.

## Estructura del Proyecto

```
/python_etl_ecommerce
|
|-- /data                   # Archivos CSV de entrada
|-- /logs                   # Archivos de log (gitignored)
|-- /output                 # Reportes Excel generados (gitignored)
|-- /src                    # Código fuente
|   |-- config.py           # Rutas, constantes y configuración
|   |-- data_loader.py      # Lógica de Extracción (E)
|   |-- transformations.py  # Lógica de Transformación (T)
|   |-- report_generator.py # Lógica de Carga (L)
|   |-- logging_config.py   # Configuración de logging
|   |-- main.py             # Orquestador principal
|
|-- /tests                  # Pruebas unitarias
|   |-- test_transformations.py
|
|-- .gitignore              # Archivos a ignorar por Git
|-- README.md               # Esta documentación
|-- requirements.txt        # Dependencias de Python
```