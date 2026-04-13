from textblob import TextBlob
import re
from collections import Counter
from deep_translator import GoogleTranslator

# ─────────────────────────────────────────────
# DICCIONARIO DE NORMALIZACIÓN DE JERGA
# Convierte contracciones y slang al inglés estándar
# para que TextBlob pueda analizarlos correctamente
# ─────────────────────────────────────────────
JERGA_A_ESTANDAR = {
    "gonna":    "going to",
    "wanna":    "want to",
    "gotta":    "got to",
    "tryna":    "trying to",
    "lemme":    "let me",
    "gimme":    "give me",
    "kinda":    "kind of",
    "sorta":    "sort of",
    "lotta":    "a lot of",
    "outta":    "out of",
    "dunno":    "do not know",
    "imma":     "i am going to",
    "cause":    "because",
    "'cause":   "because",
    "cuz":      "because",
    "bout":     "about",
    "til":      "until",
    "'til":     "until",
    "ya":       "you",
    "em":       "them",
    "'em":      "them",
    "y'all":    "you all",
    "c'mon":    "come on",
    "wassup":   "what is up",
    "woulda":   "would have",
    "coulda":   "could have",
    "shoulda":  "should have",
    "musta":    "must have",
    "ain't":    "are not",
    "doin":     "doing",
    "nothin":   "nothing",
    "somethin": "something",
    "everythin":"everything",
    "runnin":   "running",
    "comin":    "coming",
    "lovin":    "loving",
    "feelin":   "feeling",
    "talkin":   "talking",
    "walkin":   "walking",
}

def normalizar_jerga(texto):
    """
    Reemplaza slang y contracciones informales por su equivalente
    estándar en inglés para que TextBlob analice correctamente el sentimiento.
    """
    texto = texto.lower()
    for jerga, estandar in JERGA_A_ESTANDAR.items():
        texto = re.sub(r'\b' + re.escape(jerga) + r'\b', estandar, texto)
    return texto

def limpiar_texto(texto):
    """
    Limpia el texto para el conteo de frecuencias (nube de palabras):
    - Normaliza la jerga
    - Elimina signos de puntuación
    - Filtra palabras cortas
    Las stopwords se gestionan en visual.py usando WordCloud.STOPWORDS
    """
    # 1. Normalizar jerga
    texto = normalizar_jerga(texto)

    # 2. Quitar caracteres no alfabéticos
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    
    # 3. Filtrar palabras muy cortas (artículos, partículas sueltas)
    palabras = texto_limpio.split()
    filtradas = [p for p in palabras if len(p) > 2]
    
    return filtradas

def obtener_sentimiento(texto):
    """
    Traduce el texto al inglés si es necesario y analiza el sentimiento.
    Esto permite que TextBlob funcione con precisión total.
    """
    try:
        # Normalizar jerga para que TextBlob entienda mejor
        texto_normalizado = normalizar_jerga(texto)

        # Traducir al inglés (GoogleTranslator es gratuito y no necesita API Key)
        # Limitamos a los primeros 2000 caracteres para que sea rápido
        texto_en = GoogleTranslator(source='auto', target='en').translate(texto[:2000])
        
        # Analizar con TextBlob (ahora en inglés, su lenguaje nativo)
        score = TextBlob(texto_en).sentiment.polarity
        return score

    except Exception as e:
        print(f"Error en traducción/análisis: {e}")
        # Si falla la traducción, intentamos analizar el original por si acaso
        return TextBlob(normalizar_jerga(texto)).sentiment.polarity

def generar_tags(score):
    """Asigna etiquetas automáticas basadas en el puntaje de sentimiento."""
    if score > 0.4:
        return "#Energético #Alegre"
    elif score > 0.1:
        return "#Positivo #Relajado"
    elif score < -0.4:
        return "#Melancólico #Triste"
    elif score < -0.1:
        return "#Nostálgico #Deep"
    else:
        return "#Neutral"

def obtener_top_palabras(palabras, top=10):
    """Devuelve las X palabras más frecuentes."""
    return dict(Counter(palabras).most_common(top))