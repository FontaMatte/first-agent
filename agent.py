import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

MAX_ITERATIONS = 5

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "Variabile OPENROUTER_API_KEY non trovata. "
        "Controlla che il file .env esista nella cartella del progetto "
        "e contenga la riga OPENROUTER_API_KEY=la-tua-chiave"
    )

client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

def get_current_datetime() -> str:
    current_datetime = datetime.now()
    return current_datetime.strftime("%A %d/%m/%Y %H:%M")

def days_between_dates(start_date: str, end_date: str) -> int:
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    difference = end - start
    return difference.days


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description":  
                "Returns the current local day of the week, date and time in the format Weekday DD/MM/YYYY HH:MM (for example: Wednesday 30/09/2026 10:11). "
                "Use it whenever the user asks about today's date, the current time or day of the week, or when a question requires knowing the current date (for example, calculating how many days are left until an event). " 
                "You do not know the current date or time on your own, so always use this tool instead of guessing.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "days_between_dates",
            "description": 
                "Returns the number of days between two dates, as an integer. "
                "The result is positive if end_date is after start_date, and negative if it is before. "
                "Use it whenever the user asks how many days are left until a date or how many days have passed since a date. "
                "If one of the two dates is today, first call get_current_datetime to get the current date: never guess it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "The starting date, in the format DD/MM/YYYY (for example: 30/09/2026)."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The ending date, in the format DD/MM/YYYY (for example: 25/12/2026)."
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },
    },
]


available_tools = {
    "get_current_datetime": get_current_datetime,
    "days_between_dates": days_between_dates,
}

messages = [
    {"role": "system", "content": "You are a helpful assistant. When a question requires information you don't have, use the available tools instead of guessing. Always answer in Italian, clearly and concisely."},
    {"role": "user", "content": "Quanti giorni mancano a Natale?"},
]

for iteration in range(MAX_ITERATIONS):

    print(f"--- Iterazione {iteration + 1} ---")

    response = client.chat.completions.create(
        model="mistralai/ministral-14b-2512",
        messages=messages,
        tools=tools,
    )

    assistant_message = response.choices[0].message

    messages.append(assistant_message)

    if not assistant_message.tool_calls:
        print(assistant_message.content)
        break


    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name
        print(f"Tool richiesto: {tool_name}")

        arguments = json.loads(tool_call.function.arguments)

        tool_function = available_tools[tool_name]
        tool_result = tool_function(**arguments)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(tool_result)
        })

else:
    print(f"L'agente ha raggiunto il limite di {MAX_ITERATIONS} iterazioni senza arrivare a una risposta finale.")

