"""Ejecuta esto UNA vez en tu ordenador para obtener el YT_REFRESH_TOKEN.

    pip install google-auth-oauthlib
    python scripts/get_token.py client_secret.json

Se abre el navegador, inicias sesión con la cuenta del canal y autorizas.
Copia el token que imprime a GitHub Secrets (YT_REFRESH_TOKEN).
"""
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

if len(sys.argv) != 2:
    sys.exit("Uso: python scripts/get_token.py client_secret.json")

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nYT_CLIENT_ID     =", creds.client_id)
print("YT_CLIENT_SECRET =", creds.client_secret)
print("YT_REFRESH_TOKEN =", creds.refresh_token)
print("\nGuarda estos tres valores en GitHub Secrets. No los compartas con nadie.")
