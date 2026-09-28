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

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description":  
                "Returns the current local date and time in the format DD/MM/YYYY HH:MM. " ""
                "Use it whenever the user asks about today's date, the current time or day of the week, or when a question requires knowing the current date (for example, calculating how many days are left until an event). " 
                "You do not know the current date or time on your own, so always use this tool instead of guessing.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]

response = client.chat.completions.create(
    model="mistralai/ministral-14b-2512",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. When a question requires information you don't have, use the available tools instead of guessing. Always answer in Italian, clearly and concisely."},
        {"role": "user", "content": "Che giorno è oggi?"},
    ],
    tools=tools
)

print(response.model_dump_json(indent=2))