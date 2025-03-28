import os
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(app_name):
    """Configura el sistema de logs para la aplicación"""
    
    # Crear el directorio de logs si no existe
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Configurar el logger
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)
    
    # Formato de los logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para la consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Handler para archivo con rotación (5 archivos de 5MB máximo)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'), 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Añadir los handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger