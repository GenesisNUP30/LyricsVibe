import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import config

def crear_nube_palabras(diccionario_frecuencias, nombre_artista):
    """Genera una nube de palabras y la guarda como imagen."""
    nube = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis'
    ).generate_from_frequencies(diccionario_frecuencias)

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
    # Normalizamos el score para que sea visual (base 1)
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