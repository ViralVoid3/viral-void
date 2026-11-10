"""Cliente de Gemini (capa gratuita) que devuelve JSON."""
import json
import os
import time

from google import genai

_client = None


def ask_json(prompt: str, retries: int = 3):
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    last = None
    for i in range(retries):
        try:
            r = _client.models.generate_content(
                model=model,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )
            return json.loads(r.text)
        except Exception as e:  # límites de cuota, JSON roto, etc.
            last = e
            time.sleep(5 * (i + 1))
    raise last
