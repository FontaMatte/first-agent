import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
    "Variabile OPENROUTER_API_KEY non trovata. "
    "Controlla che il file .env esista nella cartella del progetto "
    "e contenga la riga OPENROUTER_API_KEY=la-tua-chiave"
)

client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

def get_current_datetime():
    current_datetime = datetime.now()
    return current_datetime.strftime("%d/%m/%Y %H:%M")

