import re
import os
import subprocess

def aumentar_volumen(video_path, factor_volumen, output_path = '' ):
    if output_path == '':
        output_path = video_path + ''
    if os.path.exists(output_path):
        output_path = nombre_final(output_path)
    print(f'{output_path=}')
    cmd = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vcodec', 'copy',
        '-af', f'"volume={factor_volumen}"',
        output_path
    ]
    print(cmd)
    subprocess.run(cmd)
    return output_path

def obtener_numero_entre_parentesis(texto):
    # Definir la expresión regular
    patron = r'\((\d+)\)'
    
    # Buscar el número en la cadena
    coincidencia = re.search(patron, texto)
    
    if coincidencia:
        # Retornar el número encontrado
        return coincidencia.group(1)
    else:
        return None

def nombre_final(output_path):

    num = obtener_numero_entre_parentesis(output_path)

    if num:
        output_path = output_path.replace(f"({num})",f"({int(num)+1})")
    else:
        x,y = os.path.splitext(output_path)
        output_path = f"{x} (1){y}"
    return output_path
def eliminar_temp(ruta):
    # Elimina la carpeta temporal
    for root, dirs, files in os.walk(ruta, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(ruta)
    
def proceso_aumentar_volumen(archivo, factor):
        # Crea una carpeta temporal para almacenar los archivos procesados
    carpeta_temporal = 'temp'
    os.makedirs(carpeta_temporal, exist_ok=True)
    ruta, archivo_nombre = os.path.split(archivo.filename)
    ruta_final = os.path.join(ruta, carpeta_temporal, archivo_nombre)
    archivo.save(ruta_final)
    print(f'{ruta_final=}')
    aumentar_volumen(ruta_final, factor)


    return ruta_final
# Llama a la función
if __name__ == "__main__":
    # Ruta al video original
    video_path = "ejemplo.mkv"

    # Ruta al video con el volumen aumentado
    output_path = "ejemplo3.mkv"

    # Factor para aumentar el volumen (ej. 2.0 para duplicar el volumen)
    factor_volumen = 3.0
    
    aumentar_volumen(video_path, factor_volumen, output_path )
