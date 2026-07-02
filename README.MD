# Resilient Fintech DataOps Core

Este repositorio contiene un pipeline ETL (Extract, Transform, Load) automatizado y resiliente, diseñado bajo estándares de **DataOps** para la ingesta y sanitización de flujos de datos financieros en tiempo real. 

El sistema está diseñado para mitigar proactivamente los dos problemas más comunes en la ingesta de datos de mercado: cortes inesperados de red y valores nulos/corruptos (data drift).

## 🚀 Arquitectura del Sistema

El proyecto aplica el principio de **Separación de Responsabilidades (Separation of Concerns)** mediante una arquitectura modular:

* `src/ingestion.py`: Simula el feed crudo del mercado inyectando fallos aleatorios (10% errores de red, 15% valores nulos).
* `src/processing.py`: Valida los tipos de datos en tiempo de ejecución usando **Pydantic** y aplica una estrategia financiera de **Forward Fill** usando **Pandas** para recuperar registros con precios nulos.
* `src/database.py`: Gestiona la persistencia local en **SQLite** aplicando almacenamiento relacional indexado (`TIMESTAMP` + `TICKER`) e idempotencia.
* `main.py`: Director de orquesta con bloques de manejo de excepciones para la mitigación activa de caídas de red.

## 🛠️ Tecnologías Utilizadas

* **Python 3.13+**
* **Pandas**: Procesamiento de datos e imputación de series temporales.
* **Pydantic**: Validación estricta de esquemas y contratos de datos.
* **SQLite3**: Almacenamiento relacional e indexación local.

## 📦 Instalación y Uso

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/resilient-fintech-dataops-core.git](https://github.com/TU_USUARIO/resilient-fintech-dataops-core.git)
   cd resilient-fintech-dataops-core