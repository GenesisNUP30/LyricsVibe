import json
import pandas as pd
from datetime import datetime, timedelta
import config

def cargar_historial_df():
    """Carga el historial.json en un DataFrame de Pandas para análisis fácil."""
    try:
        with open(config.ARCHIVO_HISTORIAL, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        if not datos:
            return None
        
        df = pd.DataFrame(datos)
        # Convertir la columna fecha de texto a objeto datetime de Python
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except Exception as e:
        print(f"Error al procesar historial: {e}")
        return None

def obtener_resumen_temporal(dias=7):
    """Filtra el historial por los últimos X días y saca conclusiones."""
    df = cargar_historial_df()
    if df is None or df.empty:
        return "No hay datos suficientes en el historial."

    # Filtrar por fecha
    fecha_limite = datetime.now() - timedelta(days=dias)
    df_filtrado = df[df['fecha'] >= fecha_limite]

    if df_filtrado.empty:
        return f"No se han analizado canciones en los últimos {dias} días."

    # Cálculos
    total_canciones = len(df_filtrado)
    artista_top = df_filtrado['artista'].mode()[0] # El que más se repite
    mood_medio = df_filtrado['mood'].mean()
    
    # Determinar Vibe general
    vibe = "Positiva" if mood_medio > 0.1 else "Melancólica" if mood_medio < -0.1 else "Neutral"

    resumen = (
        f"\n--- Resumen de los últimos {dias} días ---\n"
        f"📊 Canciones analizadas: {total_canciones}\n"
        f"👑 Artista más escuchado: {artista_top}\n"
        f"🎭 Vibe media: {vibe} ({mood_medio:.2f})"
    )
    return resumen