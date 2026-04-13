from textblob import TextBlob
import re
from collections import Counter
from deep_translator import GoogleTranslator

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
    Traduce el texto al inglés si es necesario y analiza el sentimiento.
    Esto permite que TextBlob funcione con precisión total.
    """
    try:
        # 1. Traducir al inglés (GoogleTranslator es gratuito y no necesita API Key)
        # Limitamos a los primeros 2000 caracteres para que sea rápido
        texto_en = GoogleTranslator(source='auto', target='en').translate(texto[:2000])
        
        # 2. Analizar con TextBlob (ahora en inglés, su lenguaje nativo)
        analisis = TextBlob(texto_en)
        score = analisis.sentiment.polarity
        
        return score
    except Exception as e:
        print(f"Error en traducción/análisis: {e}")
        # Si falla la traducción, intentamos analizar el original por si acaso
        return TextBlob(texto).sentiment.polarity

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