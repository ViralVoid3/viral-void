
"""Cliente de Gemini con reintentos ante errores temporales."""
import json
import os
import time
import random

from google import genai

_client = None


def ask_json(prompt: str, retries: int = 5):
    global _client

    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    last = None

    for i in range(retries):
        try:
            r = _client.models.generate_content(
                model=model,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )
            return json.loads(r.text)

        except Exception as e:
            last = e

            if i == retries - 1:
                break

            wait = min(10 * (2 ** i), 80) + random.uniform(0, 3)

            print(
                f"[Gemini] Intento {i + 1}/{retries} fallido. "
                f"Reintentando en {wait:.0f} segundos. Error: {e}",
                flush=True,
            )

            time.sleep(wait)

    raise last
