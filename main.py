from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from excel_python import agregar_a_excel
import os
import zipfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('pagina_inicio.html')

@app.route("/correos", methods = ['GET','POST'])
def correos():
    if request.method == 'POST':
        texto = request.form['texto']
        texto_eliminar = request.form['texto_eliminar']
        nuevo_texto = eliminar_texto(texto, texto_eliminar)
        print(texto_eliminar)
    return render_template('pagina_correos.html')


@app.route('/saludo/<nombre>')
def saludo(nombre):
    return "¡Hola, {}!".format(nombre)

@app.route('/pagina')
def pagina():
    return render_template('pagina.html')

@app.route('/cambio', methods=['GET', 'POST'])
def cambio():
    if request.method == 'POST':
        archivos = request.files.getlist('archivos')
        nombre = request.form.get('nombre')
        numero = request.form.get('numero')
        
        # Procesa los archivos y genera la carpeta comprimida
        carpeta_resultado = procesar_archivos(archivos, nombre, numero)
        
        # Envía la carpeta comprimida para descargar
        return send_file(carpeta_resultado, as_attachment=True)
    return render_template('formulario.html')

def procesar_archivos(archivos, nombre, numero):
    # Crea una carpeta temporal para almacenar los archivos procesados
    carpeta_temporal = 'temp'
    os.makedirs(carpeta_temporal, exist_ok=True)
    
    # Procesa los archivos y guarda los resultados en la carpeta temporal
    for i, archivo in enumerate(archivos):
        # Genera un nuevo nombre para el archivo
        nuevo_nombre = f'{nombre}_{int(numero)+i}{os.path.splitext(archivo.filename)[1]}'
        archivo_path = os.path.join(carpeta_temporal, nuevo_nombre)
        
        # Guarda el archivo con el nuevo nombre en la carpeta temporal
        archivo.save(archivo_path)
    # Comprime la carpeta temporal en un archivo ZIP
    carpeta_comprimida = 'resultado.zip'
    with zipfile.ZipFile(carpeta_comprimida, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(carpeta_temporal):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), carpeta_temporal))
    
    # Elimina la carpeta temporal
    for root, dirs, files in os.walk(carpeta_temporal, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(carpeta_temporal)
    
    return carpeta_comprimida

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verificar si se enviaron archivos en la solicitud
        if 'file' not in request.files or 'file2' not in request.files:
            return 'No se encontraron archivos en la solicitud'
        
        file = request.files['file']
        file_2 = request.files['file2']
        
        # Verificar si se seleccionaron archivos
        if file.filename == '' or file_2.filename == '':
            return 'No se seleccionaron los dos archivos requeridos'
        
        # Guardar los archivos en el servidor
        filename = secure_filename(file.filename)
        filename_2 = secure_filename(file_2.filename)
        file.save(os.path.join('uploads/', filename))
        file_2.save(os.path.join('uploads/', filename_2))
        
        # Procesar los archivos mediante la función extraer_info()
        agregar_a_excel( "uploads/resultado.xlsx", os.path.join('uploads/', filename), os.path.join('uploads/', filename_2))
        
        # Eliminar los archivos del servidor después de procesarlos
        os.remove(os.path.join('uploads/', filename))
        os.remove(os.path.join('uploads/', filename_2))
        
        # Generar el archivo de resultado y permitir su descarga
        resultado_filename = os.path.join('uploads/','resultado.xlsx')
        
        
        return send_file(resultado_filename, as_attachment=True)
    
    return render_template('horas_unidad.html')


if __name__ == '__main__':
    app.run(debug=True)
