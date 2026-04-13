from transformers import pipeline
from collections import Counter
import re

# ─────────────────────────────────────────────
# INICIALIZACIÓN DEL ANALIZADOR
# BERT multilingüe: funciona con inglés, español y mezcla de ambos.
# La primera vez descarga el modelo (~400MB), después va en caché.
# ─────────────────────────────────────────────
print("[Setup] Cargando modelo de análisis multilingüe...")
bert_sentiment = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    truncation=True,
    max_length=512
)
print("[Setup] Modelo cargado correctamente.")

# ─────────────────────────────────────────────
# DICCIONARIO DE NORMALIZACIÓN DE JERGA
# Convierte contracciones y slang al inglés estándar
# para que BERT pueda entender mejor el contexto
# ─────────────────────────────────────────────
JERGA_A_ESTANDAR = {
    "gonna":     "going to",
    "wanna":     "want to",
    "gotta":     "got to",
    "tryna":     "trying to",
    "lemme":     "let me",
    "gimme":     "give me",
    "kinda":     "kind of",
    "sorta":     "sort of",
    "lotta":     "a lot of",
    "outta":     "out of",
    "dunno":     "do not know",
    "imma":      "i am going to",
    "cause":     "because",
    "'cause":    "because",
    "cuz":       "because",
    "bout":      "about",
    "til":       "until",
    "'til":      "until",
    "ya":        "you",
    "em":        "them",
    "'em":       "them",
    "y'all":     "you all",
    "c'mon":     "come on",
    "wassup":    "what is up",
    "woulda":    "would have",
    "coulda":    "could have",
    "shoulda":   "should have",
    "musta":     "must have",
    "ain't":     "are not",
    "doin":      "doing",
    "nothin":    "nothing",
    "somethin":  "something",
    "everythin": "everything",
    "runnin":    "running",
    "comin":     "coming",
    "lovin":     "loving",
    "feelin":    "feeling",
    "talkin":    "talking",
    "walkin":    "walking",
}

def normalizar_jerga(texto):
    """
    Reemplaza slang y contracciones informales por su equivalente
    estándar en inglés para mejorar el análisis de sentimiento.
    """
    texto = texto.lower()
    for jerga, estandar in JERGA_A_ESTANDAR.items():
        texto = re.sub(r'\b' + re.escape(jerga) + r'\b', estandar, texto)
    return texto

def _convertir_bert_a_score(resultado):
    """
    BERT devuelve estrellas del 1 al 5.
    Las convertimos a escala [-1, 1] para mantener consistencia
    con el resto del sistema.
        1 estrella  → -1.0  (muy negativo)
        2 estrellas → -0.5  (negativo)
        3 estrellas →  0.0  (neutral)
        4 estrellas → +0.5  (positivo)
        5 estrellas → +1.0  (muy positivo)
    """
    estrellas = int(resultado[0]['label'][0])
    return (estrellas - 3) / 2.0

def obtener_sentimiento(texto):
    """
    Analiza el sentimiento de una letra usando BERT multilingüe.
    Al leer frases completas en contexto, distingue correctamente
    súplicas, ironías y lenguaje emocional indirecto.
    Devuelve un score entre -1.0 (muy negativo) y +1.0 (muy positivo).
    """
    try:
        # Normalizamos la jerga antes de analizar
        texto_normalizado = normalizar_jerga(texto)

        # BERT tiene un límite de 512 tokens, usamos los primeros 1000 caracteres
        resultado = bert_sentiment(texto_normalizado[:1000])
        return _convertir_bert_a_score(resultado)

    except Exception as e:
        print(f"[!] Error en análisis de sentimiento: {e}")
        return 0.0

def limpiar_texto(texto):
    """
    Limpia el texto para el conteo de frecuencias (nube de palabras):
    - Normaliza la jerga
    - Elimina signos de puntuación
    - Filtra palabras de 2 letras o menos
    Las stopwords se gestionan en visual.py con WordCloud.STOPWORDS
    """
    # 1. Normalizar jerga
    texto = normalizar_jerga(texto)

    # 2. Quitar caracteres no alfabéticos
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())

    # 3. Filtrar palabras muy cortas
    palabras = texto_limpio.split()
    filtradas = [p for p in palabras if len(p) > 2]

    return filtradas

def generar_tags(score):
    """
    Asigna etiquetas automáticas basadas en el puntaje de sentimiento.
    """
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