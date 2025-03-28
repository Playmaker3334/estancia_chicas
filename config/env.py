import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la aplicación
def get_app_config():
    return {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DEBUG': os.getenv('DEBUG', 'False').lower() in ('true', '1', 't'),
        'PORT': int(os.getenv('PORT')),
    }

# Configuración de la base de datos
def get_db_config():
    return {
        'MYSQL_HOST': os.getenv('DB_HOST'),
        'MYSQL_PORT': int(os.getenv('DB_PORT')),
        'MYSQL_USER': os.getenv('DB_USER'),
        'MYSQL_PASSWORD': os.getenv('DB_PASSWORD'),
        'MYSQL_DB': os.getenv('DB_NAME'),
    }

# Configuración de archivos
def get_upload_config():
    return {
        'UPLOAD_FOLDER': os.getenv('UPLOAD_FOLDER'),
        'MAX_CONTENT_LENGTH': int(os.getenv('MAX_CONTENT_LENGTH')),
    }