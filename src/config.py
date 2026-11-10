
"""Configuración del canal VIRAL VOID.
Contenido optimizado para YouTube Shorts en español.
"""

# --------------------------------------------------
# IDENTIDAD DEL CANAL
# --------------------------------------------------

NICHE = (
    "curiosidades sorprendentes sobre inteligencia artificial, "
    "herramientas de IA increíbles, novedades tecnológicas, "
    "experimentos digitales y noticias virales de tecnología, "
    "explicadas de forma sencilla, entretenida y sorprendente"
)

LANGUAGE = "es"

# --------------------------------------------------
# LOCUCIÓN
# --------------------------------------------------

# Voz masculina española
VOICE = "es-ES-AlvaroNeural"

# Un poco más rápida para mantener ritmo de Shorts
VOICE_RATE = "+10%"

# --------------------------------------------------
# DURACIÓN Y FORMATO
# --------------------------------------------------

# Objetivo aproximado: 45-60 segundos
# 120 palabras a un ritmo de 150 palabras/minuto = 48 segundos
TARGET_WORDS = 120

# Formato vertical 9:16
W, H = 1080, 1920

# --------------------------------------------------
# INVESTIGACIÓN DE TENDENCIAS
# --------------------------------------------------

NEWS_QUERIES = [
    "inteligencia artificial novedades",
    "nuevas herramientas inteligencia artificial",
    "ChatGPT OR Gemini OR Claude",
    "IA generativa aplicaciones sorprendentes",
    "robots inteligencia artificial tecnología",
    "experimentos inteligencia artificial",
]

# --------------------------------------------------
# PUBLICACIÓN
# --------------------------------------------------

TIMEZONE = "Europe/Madrid"

# Hora recomendada inicial para probar
DEFAULT_PUBLISH_HOUR = 18

# --------------------------------------------------
# YOUTUBE
# --------------------------------------------------

# Categoría: Ciencia y tecnología
CATEGORY_ID = "28"
