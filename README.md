

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

## 📦 Instalar dependenciass

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








# Explicación de los Archivos Modificados

## 📜 sqlscripts.yml

Este archivo YAML contiene scripts SQL mejorados para la gestión de la base de datos del Data Warehouse. Su estructura y propósito son:

### 1. **setup_cleanup**
- **Propósito**: Preparación inicial de la base de datos.
- **Contenido**:
  - Elimina constraints existentes (PKs y FKs) de las tablas de hechos para evitar conflictos.
  - Corrige tipos de datos clave (como BIGINT) para garantizar compatibilidad.
  - Maneja casos donde las columnas pueden tener valores nulos durante la transformación.

### 2. **dimensions_pk**
- **Propósito**: Establece las llaves primarias en las tablas de dimensiones.
- **Características**:
  - Añade constraints PRIMARY KEY a `dim_cliente`, `dim_mensajero`, `dim_sede` y `dim_tiempo`.
  - No modifica la estructura existente de las dimensiones.

### 3. **facts_pk**
- **Propósito**: Estrategia mejorada para PKs en tablas de hechos.
- **Innovaciones**:
  - Crea columnas artificiales (`servicio_id`, `NovedadKey`) como SERIAL para PKs robustas.
  - Índices únicos para controlar duplicados naturales (`idx_servicio_unico`).
  - Comentarios descriptivos para documentación automática.

### 4. **facts_fk_servicios/facts_fk_novedades**
- **Propósito**: Define las relaciones entre hechos y dimensiones.
- **Detalles**:
  - Constraints FOREIGN KEY que vinculan `fact_servicios` y `fact_novedades` con las dimensiones.
  - Referencias a `tiempo_key`, `ClienteKey`, `SedeKey`, etc.

### 5. **etl_strategy**
- **Propósito**: Lógica avanzada para el proceso ETL.
- **Componentes clave**:
  - Tabla de staging (`stg_servicios`) con columna `accion` para control de cambios.
  - Función `carga_servicios()` para carga incremental con detección de duplicados.
  - Función `limpiar_duplicados_servicios()` para limpieza de registros redundantes.

---

## 🐍 main.py

Script principal con mejoras significativas:

### 1. **Manejo de conexiones**
- **Nuevo**: Conexiones flexibles con soporte SSL condicional (`require_ssl`).
- **Resiliencia**: Reintenta sin SSL si falla la conexión segura.

### 2. **Funciones clave**
- **`run_notebook()`**: Ejecuta notebooks usando `nbconvert` con el mismo intérprete de Python.
- **`check_data_changes()`** (placeholder): Lógica para detectar cambios en los datos fuente.
- **`clean_etl_tables()`**: Limpieza segura de tablas usando transacciones.

### 3. **Flujo mejorado**
1. **Pre-ETL**: Verifica estado de la BD y datos.
2. **Ejecución**: Procesa notebooks en orden (dimensiones → hechos).
3. **Post-ETL**: Ejecuta scripts SQL de `sqlscripts.yml` con manejo de errores por sección.

### 4. **Manejo de errores**
- Rollback automático en fallos.
- Continuación tras errores en notebooks individuales.

---

## 📊 hecho_servicios.ipynb

Notebook especializado en la tabla de hechos de servicios:

### Proceso ETL
1. **Extracción**: 
   - Datos de `mensajeria_servicio`, `mensajeria_origenservicio`, etc.
   - Dimensiones desde el DW (`dim_cliente`, `dim_sede`).

2. **Transformación**:
   - **Tiempos**: Calcula duraciones entre fases (asignación, recogida, entrega).
   - **Eficiencia**: Métrica basada en tiempo promedio por mensajero.
   - **Prioridades**: Mapeo de valores como `Alta: En una Hora` a minutos.

3. **Carga**:
   - Subconjunto de 5,000 registros a `fact_servicios`.
   - Consultas analíticas predefinidas (ej: eficiencia por mensajero).

### Validaciones
- Verificación de nulos en timestamps.
- Imputación de medianas para duraciones faltantes.

---

## ⚠️ hecho_novedades.ipynb

Notebook para hechos de novedades:

### Flujo clave
1. **Enriquecimiento**:
   - Merge con `dim_tiempo` usando `fecha_novedad`.
   - Clasificación de gravedad (`alta`/`baja`) según `tipo_novedad_id`.

2. **Lógica de resolución**:
   - Asigna soluciones automáticas basadas en gravedad.
   - Calcula `CostoAdicional` según año y salario del mensajero.

3. **Manejo temporal**:
   - Detecta casos especiales (ej: "fecha entrada y salida son nulas").
   - Conversión robusta a `timedelta`.

### Output
- Tabla `fact_novedades` con métricas como `ContadorNovedad`.

---

## Impacto Conjunto

Estos cambios proporcionan:
✔️ **Mayor robustez**: Manejo de errores y duplicados.  
✔️ **Documentación embebida**: Comentarios en SQL y YAML.  
✔️ **Flexibilidad**: Conexiones con/sin SSL.  
✔️ **Escalabilidad**: Carga incremental vía funciones PL/pgSQL.



```

  
