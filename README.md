# Canal de YouTube de IA, automatizado y gratuito

Cada día: estudia tendencias → elige tema → escribe guion → locuta → monta el vídeo →
crea miniatura → sube a YouTube como **privado y programado** a la mejor hora.
Tú revisas en YouTube Studio antes de que se publique.

## Coste: 0 €
GitHub Actions · Gemini (capa gratuita) · edge-tts · Pexels · YouTube Data API.

## Puesta en marcha (una sola vez)

### 1. Claves gratuitas
- **Gemini:** https://aistudio.google.com/apikey → crear clave → `GEMINI_API_KEY`
- **Pexels:** https://www.pexels.com/api/ → `PEXELS_API_KEY`

### 2. Credenciales de YouTube
1. https://console.cloud.google.com → crea un proyecto.
2. *APIs y servicios → Biblioteca* → activa **YouTube Data API v3**.
3. *Pantalla de consentimiento OAuth* → tipo **Externo** → añade tu correo como usuario de prueba.
4. *Credenciales → Crear → ID de cliente OAuth → Aplicación de escritorio* → descarga el JSON
   y guárdalo como `client_secret.json` (NO lo subas a GitHub).
5. **Importante:** vuelve a la pantalla de consentimiento y pulsa **"Publicar aplicación"**
   (estado *En producción*). Si se queda en *Pruebas*, el token caduca a los 7 días y la
   automatización se rompe. Para uso personal no hace falta verificación.
6. En tu ordenador:
   ```
   pip install google-auth-oauthlib
   python scripts/get_token.py client_secret.json
   ```
   Inicia sesión con la cuenta del canal. Te imprime `YT_CLIENT_ID`, `YT_CLIENT_SECRET`
   y `YT_REFRESH_TOKEN`.
7. Verifica tu canal por teléfono en https://www.youtube.com/verify (necesario para miniaturas
   personalizadas).

### 3. GitHub
1. Crea un repositorio (si es público, los minutos de Actions son ilimitados; privado: 2.000/mes,
   de sobra para 1 vídeo diario).
2. Sube esta carpeta.
3. *Settings → Secrets and variables → Actions → New repository secret* y crea los 5 secretos:
   `GEMINI_API_KEY`, `PEXELS_API_KEY`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
4. *Settings → Actions → General → Workflow permissions* → **Read and write permissions**.

### 4. Primera prueba
*Actions → Vídeo diario → Run workflow* con **dry_run activado**. Descarga el vídeo desde
*Artifacts* y revísalo. Cuando te guste, ejecútalo con dry_run desactivado: subirá el vídeo
como privado y programado. Desde entonces corre solo cada día.

## Prueba en local
```
pip install -r requirements.txt     # y tener ffmpeg instalado
export GEMINI_API_KEY=... PEXELS_API_KEY=...
python src/main.py --dry-run
```
Resultado en `out/AAAA-MM-DD/` (vídeo, miniatura, meta.json).

## Personalizar
Edita `src/config.py`: enfoque del canal, voz, duración, zona horaria y hora por defecto.

## Límites que debes conocer
- **Proyectos de API sin auditar:** YouTube bloquea como *privados* los vídeos subidos por la API
  desde proyectos sin verificar. Si tus vídeos no se publican solos, ábrelos en YouTube Studio y
  ponlos en público a mano, o solicita la auditoría de cumplimiento de la API de YouTube.
- **Hora óptima:** YouTube Analytics no da datos por hora del día. El sistema usa tus 50 últimos
  vídeos (rendimiento según hora de publicación) cuando hay ≥10; antes usa la hora por defecto.
- **Monetización:** YouTube no paga contenido repetitivo o en masa sin aporte propio. Revisa cada
  vídeo, añade tu opinión y mejora los guiones. La automatización es para producir más rápido, no
  para dejar de pensar.
- **Cuota de Gemini gratuita:** puede cambiar; si falla, cambia el modelo con la variable
  `GEMINI_MODEL`.
- **Derechos:** Pexels permite uso comercial sin atribución, pero revisa sus condiciones.
