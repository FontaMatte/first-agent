from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()

model = ChatOpenRouter(model="mistralai/ministral-14b-2512")

response = model.invoke([
    {"role": "system", "content": "You are a helpful assistant. When a question requires information you don't have, use the available tools instead of guessing. Always answer in Italian, clearly and concisely."},
    {"role": "user", "content": "Quanti giorni mancano a Natale?"},
])

print(response)
print(response.content)