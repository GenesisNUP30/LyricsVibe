import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import config

# ─────────────────────────────────────────────
# STOPWORDS PERSONALIZADAS
# WordCloud ya trae las del inglés. Aquí añadimos:
# 1. Preposiciones y conectores en español
# 2. Muletillas típicas de canciones en ambos idiomas
# ─────────────────────────────────────────────

STOPS_ESPAÑOL = {
    # Artículos
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    # Preposiciones
    "de", "en", "a", "ante", "bajo", "con", "contra", "desde",
    "durante", "entre", "hacia", "hasta", "mediante", "para",
    "por", "según", "sin", "sobre", "tras",
    # Conectores y conjunciones
    "que", "y", "o", "pero", "sino", "porque", "aunque", "cuando",
    "como", "si", "ni", "pues", "así", "mientras", "donde",
    # Pronombres
    "yo", "tu", "el", "ella", "nos", "vos", "ellos", "ellas",
    "me", "te", "se", "mi", "mis", "su", "sus", "nuestro",
    # Verbos auxiliares comunes
    "ser", "estar", "hay", "era", "fue", "son", "han", "has",
    "tengo", "tiene", "tiene", "quiero", "quiere", "soy", "eres",
    # Otras palabras vacías frecuentes
    "más", "muy", "también", "todo", "toda", "bien", "mal",
    "aquí", "allí", "ahora", "siempre", "nunca", "solo", "ya",
    "algo", "nada", "otro", "otra", "esto", "esta", "ese", "esa",
}

MULETILLAS_CANCIONES = {
    # Inglés
    "yeah", "yea", "ooh", "ugh", "mmm", "woah", "whoa",
    "oh", "ah", "na", "hey", "like", "just", "know",
    "got", "get", "let", "said", "back", "baby", "love",
    "come", "going", "gone", "want", "need", "feel",
    # Español
    "ey", "oe", "eeh", "aah", "mami", "papi", "wei",
    "oye", "ven", "dime", "dale", "vamos", "bueno",
}

# Combinamos las stopwords de WordCloud (inglés) con las nuestras
STOPWORDS_COMPLETAS = STOPWORDS | STOPS_ESPAÑOL | MULETILLAS_CANCIONES

def crear_nube_palabras(diccionario_frecuencias, nombre_artista):
    """
    Genera una nube de palabras filtrando stopwords en inglés (WordCloud),
    español y muletillas de canciones. La guarda en outputs/ y la muestra.
    """
    # Filtramos el diccionario antes de pasárselo a WordCloud
    frecuencias_filtradas = {
        palabra: freq
        for palabra, freq in diccionario_frecuencias.items()
        if palabra.lower() not in STOPWORDS_COMPLETAS
    }

    if not frecuencias_filtradas:
        print("[!] No hay palabras suficientes para generar la nube.")
        return

    nube = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis',
        stopwords=STOPWORDS_COMPLETAS 
    ).generate_from_frequencies(frecuencias_filtradas)

    plt.figure(figsize=(10, 5))
    plt.imshow(nube, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Letras de: {nombre_artista}")
    
    # Guardar en la carpeta de outputs
    ruta_salida = os.path.join(config.CARPETA_OUTPUTS, f"nube_{nombre_artista}.png")
    plt.savefig(ruta_salida)
    plt.show()

def mostrar_dashboard(score, top_palabras):
    """Crea una ventana con el Termómetro de Ánimo y el Top 10 palabras."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 1. Termómetro de Ánimo (Gráfico de tarta)
    pos = max(0, score) if score > 0 else 0
    neg = abs(score) if score < 0 else 0
    neu = 1 - (pos + neg)
    
    ax1.pie([pos, neg, neu], labels=['Positivo', 'Negativo', 'Neutral'], 
            colors=['#66bb6a', '#ef5350', '#bdbdbd'], autopct='%1.1f%%')
    ax1.set_title("Vibe de la Canción")

    # 2. Top 10 Palabras (Barras horizontales)
    palabras = list(top_palabras.keys())
    frecuencias = list(top_palabras.values())
    
    ax2.barh(palabras, frecuencias, color='#42a5f5')
    ax2.invert_yaxis()  # La más frecuente arriba
    ax2.set_title("Palabras Clave")

    plt.tight_layout()
    plt.show()