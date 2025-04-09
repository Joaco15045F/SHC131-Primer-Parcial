# Generador Automático de CRUD en Laravel con Interfaz Tkinter

## Descripción
El **Generador Automático de CRUD en Laravel con Interfaz Tkinter** es una herramienta desarrollada en Python que automatiza la creación de aplicaciones web CRUD (Crear, Leer, Actualizar, Eliminar) basadas en Laravel y PostgreSQL. Utiliza una interfaz gráfica en Tkinter para autenticación, configuración de bases de datos y generación de proyectos Laravel completos con modelos, controladores, vistas y rutas optimizadas. Este proyecto agiliza el desarrollo web, incluyendo soporte para relaciones de claves foráneas, manejo de imágenes y DataTables dinámicos.

---

## Características Principales
- **Autenticación**: Login seguro con credenciales predefinidas.
- **Conexión a BD**: Configuración dinámica y validación para PostgreSQL.
- **Selección de Tablas**: Detección automática de tablas y relaciones.
- **Generación Automática**:
  - Modelos Eloquent con relaciones `belongsTo`.
  - Controladores RESTful con validaciones y excepciones.
  - Vistas Blade con Yajra DataTables y modales AJAX.
  - Rutas optimizadas.
- **Multimedia**: Subida y gestión de imágenes.
- **Integración**: Proyecto listo para producción con `php artisan serve`.
- **Personalización**: Selección interactiva de campos descriptivos para relaciones.

---

## Tecnologías Utilizadas
- **Python 3.8+**: Lógica y GUI.
- **Tkinter**: Interfaz gráfica.
- **psycopg2**: Conector PostgreSQL.
- **Pillow**: Manejo de imágenes.
- **Laravel 10.x**: Framework PHP.
- **PostgreSQL 14+**: Base de datos.
- **Bootstrap 5**: Estilizado.
- **Yajra DataTables**: Tablas dinámicas.
- **Composer**: Dependencias PHP.

---

## Requisitos Previos

### Software
- **Python 3.8+**: [Descargar](https://www.python.org/downloads/).
- **XAMPP 8.x**: Incluye PHP y PostgreSQL ([Descargar](https://www.apachefriends.org/es/index.html)).
- **PHP 8.1+**: Para Laravel.
- **Composer**: [Descargar](https://getcomposer.org/).
- **PostgreSQL 14+**: [Descargar](https://www.postgresql.org/download/).
- **Git**: Para clonar el repositorio.

### Dependencias de Python
Instala con:
```bash
pip install tk psycopg2-binary pillow
```

### Proyecto Laravel Base
El proyecto usa `laravel-base` (incluido en este repositorio) como plantilla:
1. Navega a `laravel-base`:
   ```bash
   cd laravel-base
   ```
2. Instala dependencias:
   ```bash
   composer install
   composer require yajra/laravel-datatables-oracle
   ```
3. Configura `.env` en `laravel-base` según tu PostgreSQL:
   ```
   DB_CONNECTION=pgsql
   DB_HOST=127.0.0.1
   DB_PORT=5432
   DB_DATABASE=crud_test
   DB_USERNAME=postgres
   DB_PASSWORD=tu_contraseña
   ```
   **Nota**: Ajusta `DB_DATABASE`, `DB_USERNAME` y `DB_PASSWORD` a tu entorno.

### Proyecto Existente (Opcional - Generar Solo Modelos)
Para generar modelos en un proyecto Laravel existente:
- Debe usar Laravel 10.x.
- Requiere `yajra/laravel-datatables-oracle` en `composer.json`. Instala con:
  ```bash
  composer require yajra/laravel-datatables-oracle
  ```
- Configura `.env` en el proyecto existente con PostgreSQL. Ejemplo:
  ```
  APP_NAME=Laravel
  APP_ENV=local
  APP_KEY=base64:O1NkZNMB5xkh4kWs+fqW6quGRQAzoSp6sf4PFPA0/N8=
  APP_DEBUG=true
  APP_URL=http://localhost

  APP_LOCALE=en
  APP_FALLBACK_LOCALE=en
  APP_FAKER_LOCALE=en_US

  APP_MAINTENANCE_DRIVER=file

  PHP_CLI_SERVER_WORKERS=4

  BCRYPT_ROUNDS=12

  LOG_CHANNEL=stack
  LOG_STACK=single
  LOG_DEPRECATIONS_CHANNEL=null
  LOG_LEVEL=debug

  DB_CONNECTION=pgsql
  DB_HOST=127.0.0.1
  DB_PORT=5432
  DB_DATABASE=dbpostgrado
  DB_USERNAME=postgres
  DB_PASSWORD=joaco123

  SESSION_DRIVER=file
  SESSION_LIFETIME=120
  SESSION_ENCRYPT=false
  SESSION_PATH=/
  SESSION_DOMAIN=null

  BROADCAST_CONNECTION=log
  FILESYSTEM_DISK=local
  QUEUE_CONNECTION=database

  CACHE_STORE=database

  MEMCACHED_HOST=127.0.0.1

  REDIS_CLIENT=phpredis
  REDIS_HOST=127.0.0.1
  REDIS_PASSWORD=null
  REDIS_PORT=6379

  MAIL_MAILER=log
  MAIL_SCHEME=null
  MAIL_HOST=127.0.0.1
  MAIL_PORT=2525
  MAIL_USERNAME=null
  MAIL_PASSWORD=null
  MAIL_FROM_ADDRESS="hello@example.com"
  MAIL_FROM_NAME="${APP_NAME}"

  AWS_ACCESS_KEY_ID=
  AWS_SECRET_ACCESS_KEY=
  AWS_DEFAULT_REGION=us-east-1
  AWS_BUCKET=
  AWS_USE_PATH_STYLE_ENDPOINT=false

  VITE_APP_NAME="${APP_NAME}"
  ```
  **Nota**: Ajusta `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, y otros valores según tu configuración.
- Ejecuta `composer install` en el proyecto existente.

---

## Instalación

### 1. Clonar el Repositorio
Clona el proyecto (incluye `Login.py`, `images/imglogin.png`, y `laravel-base`):
```bash
git clone <URL_DEL_REPOSITORIO>
```

### 2. Instalar Dependencias de Python
En la raíz del repositorio:
```bash
pip install tk psycopg2-binary pillow
```

### 3. Configurar PostgreSQL
1. Inicia PostgreSQL en XAMPP.
2. Crea una base de datos:
   ```sql
   CREATE DATABASE crud_test;
   ```
3. Añade tablas de prueba:
   ```sql
   CREATE TABLE usuarios (
       id SERIAL PRIMARY KEY,
       nombre VARCHAR(255) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL
   );
   CREATE TABLE pedidos (
       id SERIAL PRIMARY KEY,
       usuario_id INT REFERENCES usuarios(id),
       fecha DATE NOT NULL,
       total NUMERIC(10,2)
   );
   ```

### 4. Configurar el Proyecto Base
1. Navega a `laravel-base`:
   ```bash
   cd laravel-base
   ```
2. Edita `.env` con tu configuración de PostgreSQL (ejemplo):
   ```
   APP_NAME=Laravel
   APP_ENV=local
   APP_KEY=base64:O1NkZNMB5xkh4kWs+fqW6quGRQAzoSp6sf4PFPA0/N8=
   APP_DEBUG=true
   APP_URL=http://localhost
   DB_CONNECTION=pgsql
   DB_HOST=127.0.0.1
   DB_PORT=5432
   DB_DATABASE=crud_test
   DB_USERNAME=postgres
   DB_PASSWORD=tu_contraseña
   SESSION_DRIVER=file
   FILESYSTEM_DISK=local
   ```
   **Nota**: Ajusta `DB_PASSWORD` y otros valores según tu entorno.
3. Instala dependencias:
   ```bash
   composer install
   composer require yajra/laravel-datatables-oracle
   ```

### 5. Configurar XAMPP
- Inicia Apache y PostgreSQL desde el panel de XAMPP.
- Asegúrate de que PHP esté en el PATH.

---

## Uso

### 1. Iniciar la Aplicación
En la raíz del repositorio:
```bash
python Login.py
```

### 2. Autenticación
- **Usuario**: `Joaco`
- **Contraseña**: `joaco123`
- Captura:  
  ![Login](https://github.com/user-attachments/assets/5b7e0016-8fc3-42d9-83d8-4aaf329a2eb4)

### 3. Configurar la Conexión
- Ingresa:
  - **Base de datos**: `crud_test`
  - **Puerto**: `5432`
  - **Usuario**: `postgres`
  - **Contraseña**: Tu contraseña
- Haz clic en **Probar Conexión**.
- Captura:  
  ![Conexión](https://github.com/user-attachments/assets/bfdfd28b-589a-4fa3-b62b-f2b67239f6fd)

### 4. Seleccionar Tablas
- Marca las tablas con ✔.
- Captura:  
  ![image](https://github.com/user-attachments/assets/753c685e-117b-487b-9865-723cdab5a805)


### 5. Generar el Proyecto
1. Ingresa un nombre (ejemplo: `mi_crud_app`) en "Nombre/Ruta del Proyecto".
2. Elige:
   - **Crear Proyecto**: Genera un nuevo proyecto completo usando `laravel-base`. Al ejecutarse `python Login.py`, el servidor se inicia automáticamente en `http://127.0.0.1:8000` y el navegador se abre.
     ![image](https://github.com/user-attachments/assets/691c446c-4713-4944-866e-497cabb52ba6)

   - **Generar Modelos**: Añade modelos, controladores y vistas a un proyecto existente (requiere `.env` configurado como en "Requisitos Previos" y Yajra instalado). Luego, navega a la carpeta de tu proyecto Laravel y ejecuta:
     ```bash
     cd mi_proyecto_existente
     php artisan serve
     ```
     ![image](https://github.com/user-attachments/assets/5ad99b54-8c56-42a9-bdb4-bdbcf7acbfbe)


3. El servidor inicia en `http://127.0.0.1:8000`. 
- Captura:  
  ![Generado](images/laravel_home_screen.png)

### 6. Explorar la Aplicación
- Visita `http://127.0.0.1:8000`.
- Captura:  
 ![image](https://github.com/user-attachments/assets/1e5b542b-6cd2-4b63-903c-088e3f9e217c)
![image](https://github.com/user-attachments/assets/1778eeae-3f00-4c29-a0d1-0066fd2ef557)



---

## Estructura del Proyecto Generado
```
mi_crud_app/
├── app/
│   ├── Http/Controllers/<Tabla>Controller.php
│   └── Models/<Tabla>.php
├── resources/views/
│   ├── layouts/app.blade.php
│   ├── <tabla>/index.blade.php
│   └── welcome.blade.php
├── routes/web.php
├── storage/app/public/
└── .env  # Copiado de laravel-base
```

---

## Resolución de Problemas
| **Problema**                  | **Solución**                                              |
|-------------------------------|----------------------------------------------------------|
| "DataTables no carga"         | Verifica `yajra/laravel-datatables-oracle` instalado.    |
| ".env no encontrado"          | Asegúrate de que `laravel-base/.env` esté configurado.   |
| "Permission denied en storage"| Ejecuta `php artisan storage:link`.                      |
| "Tablas no aparecen"          | Confirma esquema `public` y `.env` correcto.             |

---

## Créditos
- **Autor**: Joaquín Aramayo Valdez
- **Curso**: SHC131 - Taller de Especialidad
- **Fecha**: Abril 2025

---

## Licencia
Proyecto académico para SHC131. Uso educativo exclusivo.
