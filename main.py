import os
import sys
import asyncio
import warnings
import yaml
from subprocess import run
from sqlalchemy import create_engine
import platform
import psycopg2
import pandas as pd

# Establecer la política de bucle de eventos para Windows (necesario en algunos entornos Windows)
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

warnings.filterwarnings("ignore", category=RuntimeWarning)

# Leer configuración de la conexión desde el archivo YAML
with open('./configBD/config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    config_etl = config['bodega']

# Construir la URL de conexión para la bodega ETL en Azure, con sslmode=require
url_etl = (
    f"{config_etl['driver']}://{config_etl['user']}:{config_etl['password']}@"
    f"{config_etl['host']}:{config_etl['port']}/{config_etl['db']}?sslmode=require"
)

# Crear el motor de conexión a la base de datos ETL
etl_conn = create_engine(url_etl)


def run_notebook(notebook_path):
    """
    Ejecuta un notebook de Jupyter usando el mismo intérprete (sys.executable).
    """
    print(f"Running notebook: {notebook_path}")
    run(
        [
            sys.executable,
            "-m", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "--clear-output",
            notebook_path
        ],
        check=True
    )


def check_data_changes():
    """
    Verifica si hay cambios en los datos (dimensiones y hechos).
    Retorna True si debe ejecutar nuevamente los notebooks; False en caso contrario.
    """
    # Implementa aquí la lógica real que compare timestamps, hashes, etc.
    return True  # Por defecto siempre ejecuta


def check_if_db_deleted():
    """
    Verifica si la base de datos (dimensiones y hechos) ha sido eliminada.
    Retorna True si la BD fue borrada y hay que recrear desde cero; False en caso contrario.
    """
    # Implementa la lógica adecuada para tu caso.
    return False


def clean_etl_tables():
    """
    Se conecta a la base ETL y ejecuta las sentencias de borrado definidas en 'sqlscripts2.yml'.
    """
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname=config_etl['db'],
            user=config_etl['user'],
            password=config_etl['password'],
            host=config_etl['host'],
            port=config_etl['port'],
            sslmode='require'
        )
        cur = conn.cursor()
        with open('sqlscripts2.yml', 'r', encoding='utf-8') as f:
            sql_scripts = yaml.safe_load(f)
            drop_tables_query = sql_scripts.get('drop_tables', '')
            if drop_tables_query:
                cur.execute(drop_tables_query)
        conn.commit()
    except Exception as e:
        print(f"Error al limpiar las tablas: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def main():
    clean_etl_tables()

    # Rutas a los notebooks que se deben ejecutar (dimensiones)
    notebooks = [
        os.path.join("mensajeria", "dimensiones", "dm_cliente.ipynb"),
        os.path.join("mensajeria", "dimensiones", "dm_sede.ipynb"),
        os.path.join("mensajeria", "dimensiones", "dm_tiempo.ipynb"),
        os.path.join("mensajeria", "dimensiones", "dm_mensajero.ipynb"),
        # Si en el futuro quieres incluir hechos, descomenta y ajusta estas líneas:
         
         os.path.join("mensajeria", "hechos", "hecho_novedades.ipynb"),
         #os.path.join("mensajeria", "hechos", "hecho_novedades_clustering.ipynb"),
         os.path.join("mensajeria", "hechos", "hecho_servicios.ipynb"),
         #os.path.join("mensajeria", "hechos", "hecho_novedades_clustering.ipynb")
    ]

    data_changed = check_data_changes()
    db_deleted = check_if_db_deleted()

    if not data_changed and not db_deleted:
        print("Las dimensiones y hechos ya están creados y sus registros no tienen cambios.")
        return

    if db_deleted:
        print("Las bases de datos de dimensiones y hechos han sido eliminadas, se ejecutarán los notebooks.")
    elif data_changed:
        print("Se detectaron cambios en los registros, se ejecutarán los notebooks.")

    # Ejecutar cada notebook
    for notebook in notebooks:
        print(f"Checking notebook: {notebook}")
        if os.path.exists(notebook):
            try:
                run_notebook(notebook)
            except Exception as e:
                print(f"Error al ejecutar el notebook {notebook}: {e}")
                # Si deseas abortar en caso de fallo, utiliza sys.exit(1)
        else:
            print(f"Notebook {notebook} not found.")

    # Después de ejecutar los notebooks, correr los scripts SQL finales
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname=config_etl['db'],
            user=config_etl['user'],
            password=config_etl['password'],
            host=config_etl['host'],
            port=config_etl['port'],
            sslmode='require'
        )
        cur = conn.cursor()
        with open('sqlscripts.yml', 'r', encoding='utf-8') as f:
            sql = yaml.safe_load(f)
            for key, val in sql.items():
                cur.execute(val)
                conn.commit()
    except Exception as e:
        print(f"Error al ejecutar sqlscripts.yml: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
