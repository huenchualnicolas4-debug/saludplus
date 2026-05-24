# SaludPlus - Sistema de Gestión de Reservas Médicas

Aplicación web Flask con acceso seguro a base de datos PostgreSQL, desarrollada para la asignatura de Bases de Datos Relacionales.

## Características

- Autenticación con bcrypt (12 rounds, salt automático)
- Autorización por roles: admin / recepcionista / médico
- CRUD completo: pacientes, médicos, especialidades, citas
- Protección contra inyección SQL vía SQLAlchemy ORM
- Protección CSRF en todos los formularios (Flask-WTF)
- Validación de datos del lado del servidor (WTForms)
- Interfaz responsiva con Bootstrap 5
- Listo para despliegue en Render.com con PostgreSQL

## Stack tecnológico

| Componente   | Tecnología                |
|--------------|---------------------------|
| Lenguaje     | Python 3.11+              |
| Framework    | Flask 3.0                 |
| ORM          | SQLAlchemy 2.x            |
| Base de datos| PostgreSQL 16 (SQLite en local) |
| Autenticación| Flask-Login + bcrypt      |
| Frontend     | Bootstrap 5.3             |
| Servidor WSGI| Gunicorn                  |
| Hosting      | Render.com (free tier)    |

## Ejecución local (Visual Studio Code)

### 1. Requisitos previos
- Python 3.11 o superior
- VS Code con la extensión Python instalada
- Git (opcional, para subir a GitHub)

### 2. Instalación

```bash
# Clonar o descomprimir el proyecto en una carpeta
cd saludplus

# Crear y activar entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
copy .env.example .env       # Windows
cp .env.example .env         # Mac/Linux

# Editar .env y poner una SECRET_KEY larga y aleatoria
```

### 4. Inicializar la base de datos

```bash
flask --app app init-db
```

Esto crea las tablas y un usuario administrador de prueba:
- Usuario: `admin`
- Contraseña: `Admin2024!`

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación queda disponible en: http://127.0.0.1:5000

## Despliegue en Render.com

### Opción A: con render.yaml (recomendada)

1. Crear cuenta gratuita en https://render.com
2. Subir el proyecto a un repositorio de GitHub
3. En Render: New → Blueprint → conectar el repositorio
4. Render detecta `render.yaml` y crea la app + base PostgreSQL automáticamente
5. Esperar 3-5 minutos a que termine el deploy
6. En el shell de Render ejecutar: `flask --app app init-db`
7. URL pública lista en: `https://saludplus.onrender.com`

### Opción B: manual

1. New → Web Service → conectar repositorio
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`
4. Crear PostgreSQL aparte y pegar el connection string como `DATABASE_URL`
5. Agregar `SECRET_KEY` con valor aleatorio en variables de entorno

## Estructura del proyecto

```
saludplus/
├── app.py              # Aplicación principal y rutas
├── models.py           # Modelos SQLAlchemy (5 tablas)
├── forms.py            # Formularios con validación (WTForms)
├── config.py           # Configuración por variables de entorno
├── requirements.txt    # Dependencias Python
├── render.yaml         # Configuración de Render.com
├── Procfile            # Comando de inicio
├── .env.example        # Plantilla de variables de entorno
├── .gitignore          # Archivos excluidos del repositorio
└── templates/          # Vistas HTML (Jinja2 + Bootstrap)
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── pacientes_lista.html
    ├── pacientes_form.html
    ├── medicos_lista.html
    ├── medicos_form.html
    ├── citas_lista.html
    ├── citas_form.html
    └── error.html
```

## Medidas de seguridad implementadas

| Riesgo OWASP             | Mitigación aplicada                                  |
|--------------------------|------------------------------------------------------|
| Inyección SQL (A03)      | SQLAlchemy ORM parametriza todas las consultas       |
| Fallo de autenticación (A07) | bcrypt con 12 rounds, sesiones HttpOnly + Secure  |
| Fallo de control de acceso (A01) | Decorador `@rol_requerido` en rutas críticas |
| CSRF                     | Tokens automáticos con Flask-WTF                     |
| XSS                      | Jinja2 escapa HTML por defecto                       |
| Configuración insegura (A05) | Variables de entorno, sin secretos en el código  |

## Pruebas

Para verificar protección contra inyección SQL, intenta loguearte con:
- Usuario: `admin' OR '1'='1`
- Contraseña: cualquiera

El sistema debe rechazar el intento sin error de SQL, demostrando que la consulta está parametrizada.

## Autor

Estudiante - Bases de Datos Relacionales - Semana 12
