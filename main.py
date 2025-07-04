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
import runpy  # ← necesario para ejecutar scripts .py

# Establecer la política de bucle de eventos para Windows
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

warnings.filterwarnings("ignore", category=RuntimeWarning)

# Leer configuración de la conexión desde el archivo YAML
with open('./configBD/config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    config_etl = config['bodega']

def get_db_connection(require_ssl=False):
    ssl_mode = 'require' if require_ssl else 'prefer'
    try:
        return psycopg2.connect(
            dbname=config_etl['db'],
            user=config_etl['user'],
            password=config_etl['password'],
            host=config_etl['host'],
            port=config_etl['port'],
            sslmode=ssl_mode
        )
    except psycopg2.OperationalError as e:
        if "SSL" in str(e):
            print("Advertencia: Fallo en conexión SSL, intentando sin SSL...")
            return psycopg2.connect(
                dbname=config_etl['db'],
                user=config_etl['user'],
                password=config_etl['password'],
                host=config_etl['host'],
                port=config_etl['port'],
                sslmode='disable'
            )
        raise

def get_sqlalchemy_engine(require_ssl=False):
    ssl_param = 'require' if require_ssl else 'prefer'
    url_etl = (
        f"{config_etl['driver']}://{config_etl['user']}:{config_etl['password']}@"
        f"{config_etl['host']}:{config_etl['port']}/{config_etl['db']}?sslmode={ssl_param}"
    )
    return create_engine(url_etl)

def run_script_or_notebook(path):
    print(f"🟡 Ejecutando: {path}")
    try:
        if path.endswith(".ipynb"):
            run([
                sys.executable, "-m", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--inplace",
                "--clear-output",
                path
            ], check=True)
        elif path.endswith(".py"):
            runpy.run_path(path, run_name="__main__")
        else:
            print(f"⚠️ Tipo de archivo no soportado: {path}")
    except Exception as e:
        print(f"❌ Error ejecutando {path}: {e}")

def check_data_changes():
    return True  # Puedes implementar lógica real aquí

def check_if_db_deleted():
    return False  # Puedes implementar lógica real aquí

def clean_etl_tables():
    conn = None
    cur = None
    try:
        conn = get_db_connection(require_ssl=False)
        cur = conn.cursor()
        with open('sqlscripts2.yml', 'r', encoding='utf-8') as f:
            sql_scripts = yaml.safe_load(f)
            drop_tables_query = sql_scripts.get('drop_tables', '')
            if drop_tables_query:
                cur.execute(drop_tables_query)
        conn.commit()
    except Exception as e:
        print(f"❌ Error al limpiar las tablas: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def execute_sql_scripts():
    conn = None
    cur = None
    try:
        conn = get_db_connection(require_ssl=False)
        cur = conn.cursor()
        with open('sqlscripts.yml', 'r', encoding='utf-8') as f:
            sql = yaml.safe_load(f)
            for key, val in sql.items():
                try:
                    print(f"🟢 Ejecutando script: {key}")
                    cur.execute(val)
                    conn.commit()
                except Exception as e:
                    print(f"❌ Error al ejecutar {key}: {e}")
                    conn.rollback()
    except Exception as e:
        print(f"❌ Error de conexión al ejecutar scripts SQL: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def drop_all_tables_if_exist():
    print("🔍 Verificando existencia de tablas en la base de datos de bodega...")
    conn = None
    cur = None
    try:
        conn = get_db_connection(require_ssl=False)
        cur = conn.cursor()
        cur.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public';
        """)
        tables = cur.fetchall()
        if tables:
            print(f"🗑 Eliminando {len(tables)} tablas existentes en la base de datos...")
            for table in tables:
                cur.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE;')
            conn.commit()
            print("✅ Todas las tablas fueron eliminadas de la base de datos.")
        else:
            print("✅ No se encontraron tablas existentes. Continuando con ETL...")
    except Exception as e:
        print(f"❌ Error al eliminar tablas existentes: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def main():
    etl_engine = get_sqlalchemy_engine(require_ssl=False)

    # 🔁 Eliminar todas las tablas si existen en la base de datos de bode
    drop_all_tables_if_exist()

    print("🚀 Iniciando proceso ETL optimizado...")
    clean_etl_tables()

    # 1. Ejecutar notebooks de dimensiones y hechos
    scripts_etl = [
        os.path.join("mensajeria", "dimensiones", "dm_cliente.ipynb"),
        os.path.join("mensajeria", "dimensiones", "dm_sede.ipynb"),
        os.path.join("mensajeria", "dimensiones", "dm_tiempo.ipynb"),
        os.path.join("mensajeria", "dimensiones", "dm_mensajero.ipynb"),
        os.path.join("mensajeria", "hechos", "hecho_servicios.ipynb"),
        os.path.join("mensajeria", "hechos", "hecho_novedades.ipynb"),
    ]

    data_changed = check_data_changes()
    db_deleted = check_if_db_deleted()

    if not data_changed and not db_deleted:
        print("✔️ Sin cambios detectados. Proceso ETL no requerido.")
        return

    for script in scripts_etl:
        if os.path.exists(script):
            run_script_or_notebook(script)
            print(f"✅ Finalizado: {script}")
        else:
            print(f"⚠️ Archivo no encontrado: {script}")

    # 2. Ejecutar scripts SQL después de cargar hechos y dimensiones
    print("\n🧾 Ejecutando scripts SQL finales...")
    execute_sql_scripts()

    # 3. Ejecutar notebook de DataMart
    datamart_script = os.path.join("mensajeria", "datamart", "datamart_etl_servicios.ipynb")
    if os.path.exists(datamart_script):
        run_script_or_notebook(datamart_script)
        print(f"✅ Finalizado: {datamart_script}")
    else:
        print(f"⚠️ Archivo no encontrado: {datamart_script}")

    print("✅ Proceso ETL completado con éxito.")


if __name__ == "__main__":
    main()
