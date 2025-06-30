Aquí tienes el archivo completo listo para copiar y pegar:

```markdown
# ETL de Mensajería - Carga de Hechos y Dimensiones

Este proyecto permite la ejecución automatizada de notebooks de Jupyter para la carga de datos en una base de datos PostgreSQL. Se conecta a dos bases de datos: una fuente llamada `proyecto` y una base de datos destino llamada `proyectob`, donde se almacenan las **dimensiones** y los **hechos**.

## ⚙️ Configuración de la base de datos

Debes tener instalado PostgreSQL localmente y crear las siguientes bases de datos:

1. `proyecto` - Base de datos fuente, donde se extraen los datos.
2. `proyectob` - Base de datos destino, donde se almacenan las tablas de dimensiones y hechos.

Puedes crear las bases de datos desde pgAdmin o con comandos SQL como:

```sql
CREATE DATABASE proyecto;
CREATE DATABASE proyectob;
```

## 📁 Archivo de configuración

Edita el archivo `./configBD/config.yml` y asegúrate de tener lo siguiente:

```yaml
mensajeria:
  driver: postgresql
  host: localhost
  port: 5432
  user: postgres
  password: Ec94
  db: proyecto

bodega:
  driver: postgresql+psycopg2
  host: localhost
  port: 5432
  user: postgres
  password: Ec94
  db: proyectob
```

Ajusta el usuario, contraseña o puertos si tu configuración de PostgreSQL es diferente.

## 🐍 activar entorno virtual

activa el entorno virtual (en terminal Bash):

```bash
source venv/Scripts/activate
```

En PowerShell (Windows):

```powershell
.\venv\Scripts\Activate.ps1
```

## 📦 Instalar dependencias

Asegúrate de tener el archivo `requirements.txt` en la raíz del proyecto con el siguiente contenido:

```txt
asyncio
PyYAML
psycopg2
sqlalchemy
jupyter
nbconvert
jupyter_client
jupyter_core
pandas
```

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar el script principal

Con el entorno activado y PostgreSQL funcionando, ejecuta:

```bash
python main.py
```

Este script:
- Limpia las tablas de la base de datos de destino si es necesario
- Ejecuta notebooks de Jupyter que crean y cargan las tablas de dimensiones y hechos
- Ejecuta scripts SQL finales definidos en `sqlscripts.yml`

## ✅ Requisitos previos

- Python 3.8 o superior
- PostgreSQL en funcionamiento (con las bases `proyecto` y `proyectob`)
- Visual Studio Code (opcional, recomendado)
- Librerías Python listadas en `requirements.txt`

## 📌 Notas

- Asegúrate de que `jupyter` esté instalado correctamente para ejecutar notebooks
- Verifica que los archivos `.ipynb` estén en las rutas correctas (`mensajeria/dimensiones/` y `mensajeria/hechos/`)
- Si PostgreSQL requiere SSL, el `sslmode=require` está configurado automáticamente en el script
```

Puedes copiar todo este contenido directamente y pegarlo en un nuevo archivo llamado `README.md` en tu proyecto. El formato Markdown se mantendrá correctamente para su visualización en GitHub u otras plataformas.