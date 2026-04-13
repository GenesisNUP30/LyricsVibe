import os

# Rutas principales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_BIBLIOTECA = os.path.join(BASE_DIR, "biblioteca")
CARPETA_OUTPUTS = os.path.join(BASE_DIR, "outputs")
ARCHIVO_HISTORIAL = os.path.join(BASE_DIR, "historial.json")

# Configuración visual 
COLOR_NUBE = "black"
PALETA_GRAFICOS = "viridis"