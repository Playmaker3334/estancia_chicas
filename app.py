from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import os
import time
from werkzeug.utils import secure_filename

# Importar configuraciones
from config.env import get_app_config, get_db_config, get_upload_config
from config.logs import setup_logger

# Configurar el logger
logger = setup_logger(__name__)

# Inicializar Flask
app = Flask(__name__)

# Aplicar configuraciones
app_config = get_app_config()
db_config = get_db_config()
upload_config = get_upload_config()

app.config.update(**app_config, **db_config, **upload_config)

# Asegurar que la carpeta de uploads exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar extensiones
mysql = MySQL(app)

# Funciones de utilidad
def save_file_to_disk(file):
    """Guarda un archivo en el sistema de archivos y retorna el archivo binario"""
    try:
        if not file or not file.filename:
            logger.info("No se recibió archivo o está vacío")
            return None, None
        
        # Leer el archivo para la base de datos
        archivo_binario = file.read()
        
        # Resetear el puntero del archivo
        file.seek(0)
        
        # Guardar en disco
        filename = secure_filename(file.filename)
        nombre = request.form.get('nombre', 'usuario')
        apellidos = request.form.get('apellidos', 'desconocido')
        unique_filename = f"{nombre}_{apellidos}_{int(time.time())}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        logger.info(f"Archivo guardado en: {file_path}")
        
        return archivo_binario, file_path
    except Exception as e:
        logger.error(f"Error al guardar archivo: {str(e)}")
        return None, None

def save_contact_to_db(nombre, apellidos, correo, telefono, mensaje, archivo_binario):
    """Guarda la información de contacto en la base de datos"""
    try:
        cur = mysql.connection.cursor()
        query = '''
            INSERT INTO formulario (nombre, apellidos, correo, telefono, mensaje, archivo)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cur.execute(query, (nombre, apellidos, correo, telefono, mensaje, archivo_binario))
        mysql.connection.commit()
        logger.info("Datos guardados en la base de datos correctamente")
        return True, "Datos guardados correctamente"
    except Exception as e:
        mysql.connection.rollback()
        error_msg = f"Error al guardar en la base de datos: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
    finally:
        if cur:
            cur.close()

# Rutas
@app.route('/')
def index():
    """Ruta principal que muestra la página de inicio"""
    logger.info("Página principal solicitada")
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    """Maneja el envío del formulario de contacto"""
    if request.method == 'POST':
        logger.info("Formulario POST recibido")
        response = {'status': 'error', 'message': ''}
        
        try:
            # Obtener datos del formulario
            nombre = request.form['nombre']
            apellidos = request.form['apellidos']
            correo = request.form['correo']
            telefono = request.form['telefono']
            mensaje = request.form['mensaje']
            
            logger.info(f"Datos recibidos: {nombre}, {apellidos}, {correo}, {telefono}")
            
            # Manejar el archivo
            archivo_binario = None
            if 'archivo' in request.files:
                archivo_binario, _ = save_file_to_disk(request.files['archivo'])
            
            # Guardar en la base de datos
            success, message = save_contact_to_db(
                nombre, apellidos, correo, telefono, mensaje, archivo_binario
            )
            
            response['status'] = 'success' if success else 'error'
            response['message'] = message
            
        except Exception as e:
            error_msg = f"Error al procesar el formulario: {str(e)}"
            logger.error(error_msg)
            response['message'] = error_msg

        return jsonify(response)

# Iniciar la aplicación
if __name__ == '__main__':
    logger.info(f"Iniciando aplicación Flask en puerto {app_config['PORT']}...")
    app.run(
        port=app_config['PORT'], 
        debug=app_config['DEBUG']
    )
