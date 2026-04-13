from textblob import TextBlob
import re
from collections import Counter

def limpiar_texto(texto):
    """Limpia la letra de signos de puntuación y palabras comunes."""
    # Convertir a minúsculas y quitar caracteres no alfabéticos
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    
    # Lista de palabras a ignorar (Stopwords manuales para no depender de otra librería)
    stopwords = {"que", "el", "la", "de", "en", "y", "a", "los", "las", "un", "una", 
                 "con", "por", "para", "mi", "tu", "su", "si", "no", "me", "te", "se"}
    
    palabras = texto_limpio.split()
    filtradas = [p for p in palabras if p not in stopwords and len(p) > 2]
    
    return filtradas

def obtener_sentimiento(texto):
    """
    Analiza la letra y devuelve un puntaje de -1 (muy triste) a 1 (muy alegre).
    """
    analisis = TextBlob(texto)
    # La polaridad indica el sentimiento
    return analisis.sentiment.polarity

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