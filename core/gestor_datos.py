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

def listar_artistas():
    """Devuelve una lista de las carpetas de artistas en la biblioteca."""
    if not os.path.exists(config.CARPETA_BIBLIOTECA):
        return []
    # Solo listamos directorios
    return [d for d in os.listdir(config.CARPETA_BIBLIOTECA) 
            if os.path.isdir(os.path.join(config.CARPETA_BIBLIOTECA, d))]

def analizar_biblioteca_artista(artista):
    """
    Lee todos los archivos .txt de un artista y devuelve:
    - texto_combinado: toda la letra junta para generar la nube maestra
    - num_canciones: cuántos archivos tiene guardados
    - mood_medio: la media de mood de sus registros en el historial
    """
    ruta_artista = os.path.join(config.CARPETA_BIBLIOTECA, artista)

    # 1. Leer todos los .txt de la carpeta del artista
    texto_combinado = ""
    num_canciones = 0

    try:
        archivos = [f for f in os.listdir(ruta_artista) if f.endswith(".txt")]
        num_canciones = len(archivos)

        for archivo in archivos:
            ruta_archivo = os.path.join(ruta_artista, archivo)
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                texto_combinado += f.read() + " "

    except Exception as e:
        print(f"[!] Error al leer la biblioteca de {artista}: {e}")
        return None, 0, 0.0

    # 2. Calcular mood medio desde el historial.json
    mood_medio = 0.0
    try:
        with open(config.ARCHIVO_HISTORIAL, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        # Filtramos solo los registros de este artista
        registros_artista = [r for r in datos if r["artista"] == artista]

        if registros_artista:
            mood_medio = sum(r["mood"] for r in registros_artista) / len(registros_artista)

    except Exception as e:
        print(f"[!] Error al leer el historial: {e}")

    return texto_combinado, num_canciones, mood_medio