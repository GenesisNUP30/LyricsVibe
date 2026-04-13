import os
import json
from datetime import datetime
import config

def inicializar_sistema():
    """Crea las carpetas y archivos necesarios si no existen."""
    carpetas = [config.CARPETA_BIBLIOTECA, config.CARPETA_OUTPUTS]
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"[Setup] Carpeta creada: {carpeta}")

    if not os.path.exists(config.ARCHIVO_HISTORIAL):
        with open(config.ARCHIVO_HISTORIAL, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f"[Setup] Archivo historial creado.")

def guardar_analisis(artista, titulo, letra, mood_score):
    """Guarda la letra en la biblioteca y registra el análisis en el JSON."""
    
    # 1. Crear carpeta del artista
    ruta_artista = os.path.join(config.CARPETA_BIBLIOTECA, artista.strip().title())
    if not os.path.exists(ruta_artista):
        os.makedirs(ruta_artista)

    # 2. Guardar el archivo .txt
    nombre_archivo = f"{titulo.strip().replace(' ', '_')}.txt"
    ruta_archivo = os.path.join(ruta_artista, nombre_archivo)
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(letra)

    # 3. Actualizar historial.json
    nuevo_registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "artista": artista.strip().title(),
        "titulo": titulo.strip(),
        "mood": mood_score
    }

    try:
        with open(config.ARCHIVO_HISTORIAL, 'r+', encoding='utf-8') as f:
            datos = json.load(f)
            datos.append(nuevo_registro)
            f.seek(0)
            json.dump(datos, f, indent=4)
    except Exception as e:
        print(f"Error al actualizar el historial: {e}")

    return ruta_archivo