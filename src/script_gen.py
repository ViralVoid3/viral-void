
"""Genera guiones cortos por escenas para Viral Void."""
import json

from config import NICHE, TARGET_WORDS
from llm import ask_json


def generate(topic: dict) -> dict:
    meta = ask_json(f"""Eres guionista de un canal de YouTube Shorts en español de {NICHE}.

Tema: {topic['topic']}
Ángulo: {topic['angle']}
Por qué ahora: {topic['why']}
Hechos de partida: {json.dumps(topic['key_facts'], ensure_ascii=False)}
Titulares de contexto: {json.dumps(topic['headlines'][:15], ensure_ascii=False)}

Escribe un vídeo de aproximadamente {TARGET_WORDS} palabras de locución.
Duración objetivo: entre 60 y 90 segundos.

REGLAS:
- Gancho muy potente durante los primeros 3 segundos.
- Tono cercano, dinámico, sorprendente y fácil de entender.
- No inventes cifras, citas ni fechas.
- Cada escena debe aportar información visualizable.
- Entre 6 y 9 escenas.
- Cada narración debe tener entre 10 y 25 palabras.
- Frases cortas y naturales para facilitar los subtítulos.
- Sin emojis ni marcas de formato.
- Incluye una CTA natural al final del vídeo.
- Añade una pregunta que anime a comentar.
- La CTA debe ser breve, natural y relacionada con el tema.
- No debe parecer publicidad ni interrumpir el ritmo.
- No debes decir cosas que parezcan una orden al espectador.

Devuelve JSON con esta forma exacta:
{{
 "title": "máx. 70 caracteres",
 "description": "gancho + resumen + 3 hashtags",
 "tags": ["8 a 12 etiquetas"],
 "thumbnail_text": "máx. 4 palabras en mayúsculas",
 "thumbnail_query": "descripción visual en inglés",
 "scenes": [
   {{
     "narration": "texto exacto que se locutará",
     "visual_query": "descripción en inglés de la escena"
   }}
 ]
}}

IMPORTANTE:
- Todas las escenas deben incluir narration y visual_query.
- No añadas campos adicionales.
- El texto total debe aproximarse a {TARGET_WORDS} palabras.
""")

    if not isinstance(meta, dict) or not isinstance(meta.get("scenes"), list):
        raise ValueError("Gemini no ha devuelto un guion con escenas válido.")

    for i, scene in enumerate(meta["scenes"]):
        if not isinstance(scene, dict) or not scene.get("narration"):
            raise ValueError(f"La escena {i + 1} no contiene narration.")
        if not scene.get("visual_query"):
            raise ValueError(f"La escena {i + 1} no contiene visual_query.")

    meta["title"] = meta.get("title", "Viral Void")[:100]
    return meta
