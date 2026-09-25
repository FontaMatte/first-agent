import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
    "Variabile OPENROUTER_API_KEY non trovata. "
    "Controlla che il file .env esista nella cartella del progetto "
    "e contenga la riga OPENROUTER_API_KEY=la-tua-chiave"
)

# 4. Crea il client OpenAI puntato su OpenRouter
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# 5. Chiama il modello con un messaggio "user": "Ciao, chi sei?"
response = client.chat.completions.create(
    model="mistralai/ministral-14b-2512",
    messages=[
        {"role": "user", "content": "Ciao, chi sei?"}
    ]
)

# 6. Stampa l'oggetto risposta COMPLETO
print(response.model_dump_json(indent=2))

# 7. Stampa solo il testo della risposta
print(response.choices[0].message.content)