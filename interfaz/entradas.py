import pyperclip
from tkinter import filedialog, Tk
import os

def capturar_portapapeles():
    """Recupera el texto que el usuario tenga copiado en el portapapeles."""
    try:
        texto = pyperclip.paste()
        if not texto.strip():
            print("\n[!] El portapapeles está vacío.")
            return None
        return texto
    except Exception as e:
        print(f"\n[!] Error al acceder al portapapeles: {e}")
        return None

def seleccionar_archivo_local():
    """Abre una ventana de Windows/Mac para seleccionar un archivo .txt."""
    # Ocultamos la ventana principal de Tkinter que sale por defecto
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True) # Hace que la ventana salga al frente

    ruta_archivo = filedialog.askopenfilename(
        title="LyricsVibe - Selecciona una letra",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    
    root.destroy() # Cerramos la instancia de Tkinter

    if ruta_archivo:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"\n[!] No se pudo leer el archivo: {e}")
    return None

def pedir_metadatos():
    """Solicita al usuario el artista y el título de la canción."""
    print("\n--- Información de la Canción ---")
    artista = input("Introduce el nombre del Artista: ").strip()
    titulo = input("Introduce el título de la Canción: ").strip()
    
    # Control de errores básico: evitar campos vacíos
    if not artista or not titulo:
        print("[!] El artista y el título son obligatorios.")
        return None, None
    
    return artista, titulo