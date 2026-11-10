"""Configuración del canal. Edita aquí lo que quieras cambiar."""

NICHE = "noticias y herramientas de inteligencia artificial explicadas fácil"
LANGUAGE = "es"

# Voz gratuita de Microsoft Edge (España, masculina). Alternativas:
# es-ES-ElviraNeural (femenina), es-MX-JorgeNeural (México)
VOICE = "es-ES-AlvaroNeural"
VOICE_RATE = "+5%"

# Duración objetivo: ~150 palabras por minuto -> 900-1100 palabras = 6-7 min
TARGET_WORDS = 1000

# Búsquedas para detectar noticias y tendencias
NEWS_QUERIES = [
    "inteligencia artificial",
    "ChatGPT OR Gemini OR Claude",
    "nueva herramienta IA",
]

# Zona horaria de tu audiencia y hora por defecto (sin datos todavía)
TIMEZONE = "Europe/Madrid"
DEFAULT_PUBLISH_HOUR = 18

# Categoría de YouTube: 28 = Ciencia y tecnología
CATEGORY_ID = "28"

W, H = 1920, 1080
