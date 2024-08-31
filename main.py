from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from excel_python import agregar_a_excel
import os
from funciones import procesar_archivos, eliminar_texto
from aumentar_volumen import proceso_aumentar_volumen

app = Flask(__name__)

mime_types_video = {
    '.mp4': 'video/mp4',
    '.avi': 'video/x-msvideo',
    '.mkv': 'video/x-matroska',
    '.webm': 'video/webm',
    '.mov': 'video/quicktime',
    '.flv': 'video/x-flv',
    '.wmv': 'video/x-ms-wmv',
    '.mpeg': 'video/mpeg',
    '.mpg': 'video/mpeg',
    '.3gp': 'video/3gpp',
    '.ogg': 'video/ogg',
}


@app.route("/")
def index():
    return render_template('pagina_inicio.html', nombre="Sebastian")


@app.route("/subir_volumen", methods = ['GET','POST'])
def subir_volumen_route():
    if request.method == 'POST':
        archivo = request.files.getlist('archivo')[0]
        factor = request.form.get('numero')
        print(archivo.filename)
        archivo_resultado = proceso_aumentar_volumen(archivo, factor=factor)
        extension = os.path.splitext( archivo_resultado)[1]
        return send_file(archivo_resultado, as_attachment=True, mimetype=mime_types_video[extension])

    return render_template('pagina_subir_volumen.html')

@app.route("/correos", methods = ['GET','POST'])
def correos():
    if request.method == 'POST':
        texto = request.form['texto']
        texto_eliminar = request.form['texto_eliminar']
        nuevo_texto = eliminar_texto(texto, texto_eliminar)
        print(nuevo_texto)
    return render_template('pagina_correos.html')


@app.route('/saludo/<nombre>')
def saludo(nombre):

    return {
        "message":"¡Hola, {}!".format(nombre)
    }

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
    app.run(debug=True, host='0.0.0.0')

