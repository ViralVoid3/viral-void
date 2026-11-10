"""Genera guion por escenas, título, descripción y etiquetas."""
import json

from config import NICHE, TARGET_WORDS
from llm import ask_json


def generate(topic: dict) -> dict:
    meta = ask_json(f"""Eres guionista de un canal de YouTube en español de {NICHE}.
Tema: {topic['topic']}
Ángulo: {topic['angle']}
Por qué ahora: {topic['why']}
Hechos de partida: {json.dumps(topic['key_facts'], ensure_ascii=False)}
Titulares de contexto: {json.dumps(topic['headlines'][:15], ensure_ascii=False)}

Escribe un vídeo de unas {TARGET_WORDS} palabras de locución (6-7 min).
Reglas:
- Tono cercano, claro y con opinión propia; evita relleno. Gancho potente en las 2 primeras frases.
- No inventes cifras, citas ni fechas. Si algo no es seguro, dilo con cautela.
- Aporta análisis útil: qué significa, a quién afecta, qué puede hacer el espectador.
- Cierra con un resumen y una pregunta para comentarios.
- 12 a 16 escenas; cada narración de 40-90 palabras, sin emojis ni marcas de formato.

Devuelve JSON con esta forma exacta:
{{
 "title": "máx. 70 caracteres, con curiosidad y palabra clave",
 "description": "gancho + resumen + 3 hashtags al final",
 "tags": ["8 a 12 etiquetas"],
 "thumbnail_text": "máx. 4 palabras en mayúsculas",
 "thumbnail_query": "búsqueda en inglés de una foto de fondo",
 "scenes": [{{"narration": "texto locutado", "visual_query": "búsqueda en inglés para vídeo de archivo"}}]
}}""")
    meta["title"] = meta["title"][:100]
    return meta
