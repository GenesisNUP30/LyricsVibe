# LyricsVibe 🎵 - Analizador de Inteligencia Musical

**LyricsVibe** es una aplicación de escritorio desarrollada en Python que permite realizar minería de datos sobre letras de canciones, analizando sentimientos y generando visualizaciones estadísticas.

## 🛠️ Tecnologías y Librerías

### Módulos Estándar 
- **os / pathlib**: Utilizados para la gestión automatizada de archivos y la estructura de directorios por artista.
- **json**: Implementado para garantizar la persistencia de datos del historial de usuario.
- **datetime**: Crucial para el filtrado temporal de estadísticas (semanal/mensual).

### Librerías Externas 
- `textblob`: Procesamiento de lenguaje natural y análisis de sentimientos.
- `wordcloud`: Generación de nubes de palabras visuales.
- `matplotlib`: Creación de dashboards y gráficos estadísticos.
- `pandas`: Manejo y filtrado de grandes volúmenes de datos del historial.
- `pyperclip`: Captura de datos en tiempo real desde el portapapeles.

## ⌨️ Funcionalidades de Entrada
- **Captura Inteligente:** Integración con el portapapeles del sistema para análisis rápido sin archivos intermedios.
- **Explorador Nativo:** Uso de ventanas de diálogo del sistema operativo para una selección de archivos intuitiva.
- **Normalización de Datos:** El sistema limpia y formatea automáticamente los nombres de artistas y archivos para mantener la biblioteca organizada.