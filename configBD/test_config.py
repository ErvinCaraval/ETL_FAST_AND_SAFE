import yaml
import psycopg2

# Función para cargar el archivo config.yml
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Función para verificar la conexión a la base de datos
def check_connection(config):
    try:
        # Crear la conexión
        connection = psycopg2.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['db']
        )
        cursor = connection.cursor()
        # Ejecutar una simple consulta para verificar la conexión
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Conexión exitosa a la base de datos {config['db']}: {db_version[0]}")
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Error conectando a la base de datos {config['db']}: {error}")

# Ruta al archivo config.yml
config_path = './configBD/config.yml'

# Cargar configuración
config = load_config(config_path)

# Verificar la conexión para 'fuente'
print("Verificando conexión a 'fuente'...")
check_connection(config['mensajeria'])