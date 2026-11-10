"""Estudio de mercado diario: noticias + tendencias + competencia en YouTube."""
import json
import urllib.parse
from datetime import datetime, timedelta, timezone

import feedparser

from config import NEWS_QUERIES, NICHE
from llm import ask_json


def google_news(query: str, n: int = 12):
    url = (
        "https://news.google.com/rss/search?q="
        + urllib.parse.quote(query + " when:2d")
        + "&hl=es&gl=ES&ceid=ES:es"
    )
    feed = feedparser.parse(url)
    return [e.title for e in feed.entries[:n]]


def rising_searches():
    """Búsquedas en alza en Google Trends (si falla, se ignora)."""
    try:
        from pytrends.request import TrendReq

        pt = TrendReq(hl="es-ES", tz=60)
        pt.build_payload(["inteligencia artificial"], timeframe="now 7-d", geo="ES")
        rising = pt.related_queries()["inteligencia artificial"]["rising"]
        return rising["query"].head(10).tolist() if rising is not None else []
    except Exception as e:
        print(f"[research] Trends no disponible: {e}")
        return []


def competition(yt, query: str):
    """Vídeos más vistos de los últimos 14 días sobre la búsqueda."""
    if yt is None:
        return []
    try:
        after = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")
        res = yt.search().list(
            part="snippet", q=query, type="video", order="viewCount",
            publishedAfter=after, regionCode="ES", relevanceLanguage="es", maxResults=5,
        ).execute()
        ids = [i["id"]["videoId"] for i in res.get("items", [])]
        if not ids:
            return []
        vids = yt.videos().list(part="snippet,statistics", id=",".join(ids)).execute()["items"]
        return [
            {"title": v["snippet"]["title"], "views": int(v["statistics"].get("viewCount", 0))}
            for v in vids
        ]
    except Exception as e:
        print(f"[research] Competencia no disponible: {e}")
        return []



def choose_topic(history, yt=None):
    headlines = []
    for q in NEWS_QUERIES:
        headlines += google_news(q)
    headlines = list(dict.fromkeys(headlines))
    rising = rising_searches()
    recent = [h["topic"] for h in history[-30:]]

    raw_cands = ask_json(f"""Eres analista de mercado de un canal de YouTube de {NICHE}, en español.
Titulares de las últimas 48 h:
{json.dumps(headlines, ensure_ascii=False)}
Búsquedas en alza: {json.dumps(rising, ensure_ascii=False)}
Temas ya publicados (NO repetir): {json.dumps(recent, ensure_ascii=False)}

Propón 5 temas de vídeo con alta demanda potencial. Devuelve JSON:
{{"candidates":[{{"topic":"...","search_query":"consulta corta para buscar en YouTube"}}]}}""")

    # Acepta tanto {"candidates": [...]} como una lista directa.
    if isinstance(raw_cands, dict):
        cands = raw_cands.get("candidates", [])
    elif isinstance(raw_cands, list):
        cands = raw_cands
    else:
        raise ValueError("Gemini no ha devuelto una lista de candidatos válida.")

    cands = [
        c for c in cands
        if isinstance(c, dict) and c.get("topic") and c.get("search_query")
    ][:5]

    if not cands:
        raise ValueError("Gemini no ha devuelto candidatos con topic y search_query.")

    for c in cands:
        c["competition"] = competition(yt, c["search_query"])

    final = ask_json(f"""Eres analista de mercado de un canal de YouTube de {NICHE}.
Candidatos con los vídeos que ya compiten (últimos 14 días):
{json.dumps(cands, ensure_ascii=False)}
Titulares de apoyo:
{json.dumps(headlines, ensure_ascii=False)}

Elige UN tema: mucha demanda y competencia débil, o con un ángulo diferenciador claro.
Usa solo hechos que aparezcan en los titulares; no inventes datos.
Devuelve JSON: {{"topic":"...","angle":"ángulo propio y diferenciador","why":"por qué ahora","key_facts":["hecho 1","hecho 2"]}}""")

    if not isinstance(final, dict):
        raise ValueError("Gemini no ha devuelto el tema final como objeto JSON.")

    final["headlines"] = headlines
    return final
