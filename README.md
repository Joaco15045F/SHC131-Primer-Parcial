# Generador Automático de CRUD en Laravel con Interfaz Tkinter


## Descripción
El **Generador Automático de CRUD en Laravel con Interfaz Tkinter** es una herramienta avanzada desarrollada en Python que automatiza la creación de aplicaciones web CRUD (Crear, Leer, Actualizar, Eliminar) basadas en Laravel, conectadas a una base de datos PostgreSQL. A través de una interfaz gráfica construida con Tkinter, los usuarios pueden autenticarse, configurar conexiones a bases de datos, seleccionar tablas y generar un proyecto Laravel completo con modelos, controladores, vistas y rutas optimizadas. Este proyecto está diseñado para acelerar el desarrollo de aplicaciones web, ofreciendo soporte para relaciones de claves foráneas, manejo de archivos y una experiencia de usuario dinámica con DataTables.

Es ideal para desarrolladores que buscan prototipar rápidamente sistemas administrativos o para estudiantes que desean explorar la integración entre Python y frameworks PHP como Laravel.

---

## Características Principales
- **Autenticación Segura**: Ventana de login con credenciales predefinidas para acceso controlado.
- **Conexión Dinámica**: Configuración y validación de conexiones a bases de datos PostgreSQL.
- **Selección de Tablas**: Interfaz interactiva para elegir tablas y detectar relaciones automáticamente.
- **Generación Automática**:
  - Modelos Eloquent con relaciones `belongsTo` basadas en claves foráneas.
  - Controladores RESTful con validaciones personalizadas y manejo de excepciones.
  - Vistas Blade con Yajra DataTables, modales AJAX y formularios dinámicos.
  - Rutas Laravel con nombres optimizados y parámetros acortados.
- **Soporte Multimedia**: Subida y gestión de imágenes para campos específicos.
- **Integración Completa**: Proyecto Laravel listo para producción con `php artisan serve`.
- **Personalización**: Elección de campos descriptivos para relaciones foráneas mediante diálogos interactivos.

---

## Tecnologías Utilizadas
- **Python 3.8+**: Lenguaje principal para la lógica de generación y la interfaz.
- **Tkinter**: Biblioteca para la interfaz gráfica de usuario.
- **psycopg2**: Conector para PostgreSQL en Python.
- **PIL (Pillow)**: Manejo de imágenes en la interfaz.
- **Laravel 10.x**: Framework PHP para el backend generado.
- **PostgreSQL**: Sistema de gestión de bases de datos relacionales.
- **Bootstrap 5**: Estilizado de las vistas generadas.
- **Yajra DataTables**: Tablas dinámicas server-side en las vistas CRUD.
- **Composer**: Gestión de dependencias PHP.

---

## Requisitos Previos
Antes de instalar y ejecutar el proyecto, asegúrate de cumplir con los siguientes requisitos:

### Software
- **Python 3.8 o superior**: [Descargar aquí](https://www.python.org/downloads/).
- **XAMPP 8.x**: Incluye PHP y soporte para PostgreSQL ([Descargar](https://www.apachefriends.org/es/index.html)).
- **PHP 8.1+**: Requerido por Laravel.
- **Composer**: Gestor de dependencias PHP ([Descargar](https://getcomposer.org/)).
- **PostgreSQL 14+**: Base de datos relacional ([Descargar](https://www.postgresql.org/download/)).
- **Git**: Para control de versiones (opcional).

### Dependencias de Python
Instala las siguientes librerías mediante `pip`:
```bash
pip install tk psycopg2-binary pillow
```

### Proyecto Laravel Base
El proyecto generado hereda gran parte de su configuración del archivo `.env` de un proyecto Laravel base ubicado en la misma carpeta de tu proyecto a generar. Este archivo es crítico para definir la conexión a la base de datos y otras configuraciones iniciales.

- **Preparar el Proyecto Base**:
  1. Crea un proyecto Laravel limpio:
     ```bash
     composer create-project laravel/laravel laravel-base
     ```
  2. Mueve la carpeta `laravel-base` a la misma donde quieres que se genere el proyecto.
  3. Instala las dependencias necesarias, incluyendo Yajra DataTables:
     ```bash
     cd C:\xampp\htdocs\carpeta_a_usar\laravel-base
     composer install
     composer require yajra/laravel-datatables-oracle
     ```
  4. Configura el archivo `.env` en `laravel-base` con una conexión a PostgreSQL (ejemplo más adelante en "Instalación").


### Proyecto Existente (para "Generar Modelos")
Si optas por generar solo modelos en un proyecto Laravel existente:
- El proyecto debe tener Laravel 10.x instalado.
- Debe incluir las siguientes dependencias en `composer.json`:
  - `yajra/laravel-datatables-oracle` para soporte de DataTables.
  - Dependencias estándar de Laravel (como `laravel/framework`).
- El archivo `.env` del proyecto existente debe estar configurado con una conexión válida a PostgreSQL.
- Ejecuta `composer install` en el proyecto existente para asegurar que todas las dependencias estén disponibles.

---

## Instalación

### Paso 1: Descargar el Proyecto
1. Clona o descarga este proyecto en un directorio accesible:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
   O copia `Login.py` a `C:\xampp\htdocs\carpeta_a_usar\`.

### Paso 2: Configurar la Imagen de Login
1. Crea una carpeta `images` en el mismo directorio que `Login.py`.
2. Coloca una imagen llamada `imglogin.png` (recomendado: 150x165 píxeles).

### Paso 3: Instalar Dependencias de Python
Ejecuta:

```bash
pip install tk psycopg2-binary pillow
```

### Paso 4: Configurar PostgreSQL
1. Inicia PostgreSQL en XAMPP o tu servidor local.
2. Crea una base de datos de prueba:
   ```sql
   CREATE DATABASE crud_test;
   ```
3. Añade tablas de ejemplo:
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

### Paso 5: Configurar el Proyecto Laravel Base
1. Asegúrate de que `C:\xampp\htdocs\carpeta_a_usar\laravel-base` exista.
2. Edita el archivo `.env` en `laravel-base` con tu configuración de PostgreSQL:
   ```env
   APP_NAME=Laravel
    APP_ENV=local
    APP_KEY=base64:O1NkZNMB5xkh4kWs+fqW6quGRQAzoSp6sf4PFPA0/N8=
    APP_DEBUG=true
    APP_URL=http://localhost
    
    APP_LOCALE=en
    APP_FALLBACK_LOCALE=en
    APP_FAKER_LOCALE=en_US
    
    APP_MAINTENANCE_DRIVER=file
    # APP_MAINTENANCE_STORE=database
    
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
    # CACHE_PREFIX=
    
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
   **Nota**: Este `.env` será copiado al nuevo proyecto generado, asegurando que la conexión a la base de datos esté preconfigurada. Aqui te dejo un ejemplo que si funciona, asegúrate de que este igual o en basea tu base de datos y configuraciones

3. Instala Yajra DataTables:
   ```bash
   composer require yajra/laravel-datatables-oracle
   ```

### Paso 6: Configurar XAMPP
1. Inicia Apache y PostgreSQL desde el panel de control de XAMPP.
2. Asegúrate de que PHP esté en el PATH del sistema.

---

## Uso

### Paso 1: Iniciar la Aplicación
Ejecuta:
```bash
python Login.py
```

### Paso 2: Autenticación
- Ingresa:
  - **Usuario**: `Joaco`
  - **Contraseña**: `joaco123`
- Captura:  
  ![image](https://github.com/user-attachments/assets/5b7e0016-8fc3-42d9-83d8-4aaf329a2eb4)


### Paso 3: Configurar la Conexión
1. Ingresa los datos de conexión (coincidentes con el `.env` de `laravel-base`):
   - **Base de datos**: `crud_test`
   - **Puerto**: `5432`
   - **Usuario**: `postgres`
   - **Contraseña**: Tu contraseña
2. Haz clic en **Probar Conexión**.
- Captura:  
  ![image](https://github.com/user-attachments/assets/bfdfd28b-589a-4fa3-b62b-f2b67239f6fd)


### Paso 4: Seleccionar Tablas
1. Marca las tablas deseadas con ✔.
- Captura:  
  ![Selección de Tablas](images/table_selection_screen.png)

### Paso 5: Generar el Proyecto o Modelos
1. Ingresa un nombre/ruta en "Nombre/Ruta del Proyecto" (ejemplo: `mi_crud_app`).
2. Opciones:
   - **Crear Proyecto**: Genera un nuevo proyecto Laravel completo, heredando el `.env` de `laravel-base`.
   - **Generar Modelos**: Añade modelos, controladores y vistas a un proyecto existente.  
     **Requisito**: El proyecto existente debe tener `yajra/laravel-datatables-oracle` instalado y un `.env` configurado.
3. El servidor se inicia en `http://127.0.0.1:8000`.
- Captura:  
  ![Proyecto Generado](images/laravel_home_screen.png)

### Paso 6: Explorar la Aplicación
- Abre `http://127.0.0.1:8000` y navega por los módulos CRUD.
- Captura:  
  ![Vista CRUD](images/crud_view_screen.png)

---

## Estructura del Proyecto Generado
```
mi_crud_app/
├── app/
│   ├── Http/
│   │   └── Controllers/
│   │       └── <Tabla>Controller.php
│   └── Models/
│       └── <Tabla>.php
├── resources/
│   └── views/
│       ├── layouts/
│       │   └── app.blade.php
│       ├── <tabla>/
│       │   └── index.blade.php
│       └── welcome.blade.php
├── routes/
│   └── web.php
├── storage/
│   └── app/public/
└── .env  # Heredado de laravel-base
```


---

## Resolución de Problemas

| **Problema**                          | **Solución**                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------|
| "DataTables no carga"                 | Asegúrate de que `yajra/laravel-datatables-oracle` esté en el proyecto.     |
| ".env no encontrado"                  | Verifica que `laravel-base` tenga un `.env` válido antes de generar.        |
| "Permission denied en storage"        | Ejecuta `php artisan storage:link` en el proyecto generado.                 |
| "Tablas no aparecen"                  | Confirma que estén en el esquema `public` y el `.env` sea correcto.         |

---

## Créditos
- **Autor**: Joaquín Aramayo Valdez
- **Curso**: SHC131 - Taller de Especialidad
- **Fecha**: Abril 2025

---

## Licencia
Proyecto académico para SHC131. Uso exclusivo educativo.

---

## Galería de Imágenes
Guarda en `images/`:
1. `banner.png`
2. `login_screen.png`
3. `db_config_screen.png`
4. `table_selection_screen.png`
5. `laravel_home_screen.png`
6. `crud_view_screen.png`
