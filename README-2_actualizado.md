# Entorno PostgreSQL y pgAdmin con Docker

Este README explica, paso a paso y de manera simple, cómo levantar un entorno con PostgreSQL y pgAdmin usando Docker, y cómo importar una base de datos desde un archivo SQL comprimido.

## 🧰 Requisitos previos

- Tener instalado **Docker** y **Docker Compose** en tu máquina.
- Estar dentro de la carpeta `postgres+pgadmin` que está dentro del proyecto `ETL_FAST_AND_SAFE`.
- Asegurarse de que `postgres+pgadmin` contiene:
  - `docker-compose.yml`
  - `copia_bd.7z`

---

## 🚀 1. Levantar los servicios de PostgreSQL y pgAdmin

1. Abre una terminal.
2. Navega a la carpeta `postgres+pgadmin`:

   ```bash
   cd postgres+pgadmin
   ```

3. Ejecuta el siguiente comando para construir y levantar los contenedores:

   ```bash
   docker-compose up --build
   ```

4. Espera mientras se descargan las imágenes y se crean los contenedores.

---

## 🌐 2. Acceder a pgAdmin desde el navegador

1. Abre tu navegador web preferido.
2. Ingresa la siguiente dirección:

   ```
   http://localhost:5050
   ```

3. Verás la pantalla de inicio de sesión de **pgAdmin**.
4. Usa las siguientes credenciales por defecto:

   - **Email:** `admin@admin.com`
   - **Password:** `admin`

5. Haz clic en **Login**.

---

## 🔧 3. Crear un servidor en pgAdmin

1. Haz clic derecho sobre **Servers** en el panel izquierdo.
2. Selecciona **Create > Server...**
3. En la pestaña **General**:
   - **Name:** `MiPostgres` (puedes poner otro si prefieres)
4. En la pestaña **Connection**:
   - **Host name/address:** `postgres_db`  
   - **Port:** `5432`
   - **Username:** `postgres`
   - **Password:** `Ec94`
   - (Opcional) Marca **Save password**
5. Haz clic en **Save**

---

## 🗃️ 4. Crear una base de datos vacía

1. En el panel izquierdo, expande `MiPostgres > Databases`.
2. Haz clic derecho sobre **Databases**.
3. Selecciona **Create > Database...**
4. En **General > Database**:
   - **Database name:** `mi_base_datos` (elige el nombre que desees)
5. Haz clic en **Save**

---

## 📥 5. Importar la base de datos desde `copia_bd.sql`

1. Descomprime el archivo `copia_bd.7z` para obtener `copia_bd.sql`.

   - En **Linux/macOS** (si tienes instalado `p7zip`):

     ```bash
     7z x copia_bd.7z
     ```

   - En **Windows** (usando **WinRAR** o **7-Zip**):
     - Haz clic derecho sobre `copia_bd.7z` > **Extraer aquí**

2. Verifica que ahora exista el archivo `copia_bd.sql` en la carpeta `postgres+pgadmin`.

3. Abre una nueva terminal desde **Visual Studio Code** (o cualquier otra terminal):

   ```bash
   cd postgres+pgadmin
   ```

4. Copia y pega los comandos contenidos en el archivo `comandos.txt`  que esta en la carpeta datos-init. Dentro de la  terminal para cargar la base de datos.

---

## ✅ ¡Todo Listo!

Ahora tienes:

- Un entorno funcional con PostgreSQL y pgAdmin en Docker
- Tu base de datos cargada desde `copia_bd.sql`

---

## 🐞 ¿Problemas?

- Revisa los logs con:

  ```bash
  docker-compose logs
  ```

- Verifica que los datos de conexión (usuario, contraseña, host) coincidan con los del archivo `docker-compose.yml`.

---

## 📁 Estructura esperada

```
ETL_FAST_AND_SAFE/
└── postgres+pgadmin/
    ├── docker-compose.yml
    ├── datos-init/
    │   ├── copia_bd.7z
    │   ├──  copia_bd.sql  ← (después de descomprimir)
    │    
    └── comandos.txt
```
