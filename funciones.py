import zipfile
import os

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


#Falta validar salto de linea y esas cosas
def eliminar_texto(texto, texto_eliminar):
    correos = texto.split(",")
    print("Correos: ", correos)
    texto_elim = texto_eliminar.split(",")

    resultado = [x+"," for x in correos if x not in texto_elim]

    return resultado