# ETL_FAST_AND_SAFE 🚚📦

Este proyecto implementa un sistema ETL (Extract, Transform, Load) para procesar y trasladar los datos desde la base de datos operativa `mensajeria_bd` hacia una base de datos de bodega `bodega`, con el objetivo de realizar análisis y reportes de forma eficiente.

---

## 📁 Estructura del proyecto
```bash
etl_fast_and_safe/
├── etl/
│ ├── extract.py # Extracción de datos desde mensajeria_bd
│ ├── transform.py # Limpieza y transformación
│ ├── load.py # Carga hacia base de datos bodega
├── config.yml # Configuración de conexión a bases de datos
├── main.py # Script principal para ejecutar el ETL
├── requirements.txt # Dependencias del proyecto
├── README.md # Este archivo
```

---

## ⚙️ Requisitos

- Python 3.10 o superior
- PostgreSQL en funcionamiento
- Acceso a las bases de datos:
  - `mensajeria_bd`
  - `bodega`

---

## 🧪 Instalación del proyecto

1. **Clonar el repositorio o descargar el código**

2. **Crear un entorno virtual (opcional pero recomendado)**

```bash
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
```
3. **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar tus credenciales en config.yml**
```bash
CO_SA:
  drivername: postgresql
  user: tu_usuario
  password: tu_contraseña
  host: localhost
  port: 5432
  dbname: mensajeria_bd

ETL_PRO:
  drivername: postgresql
  user: tu_usuario
  password: tu_contraseña
  host: localhost
  port: 5432
  dbname: bodega

  ```

5. **🚀 Ejecución del ETL**
```bash
python main.py
  ```
