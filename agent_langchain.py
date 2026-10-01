from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openrouter import ChatOpenRouter

load_dotenv()

model = ChatOpenRouter(model="mistralai/ministral-14b-2512")

@tool(parse_docstring=True)
def get_current_datetime() -> str:
    """Returns the current local day of the week, date and time in the format
    Weekday DD/MM/YYYY HH:MM (for example: Wednesday 30/09/2026 10:11).
    Use it whenever the user asks about today's date, the current time or day
    of the week, or when a question requires knowing the current date (for
    example, calculating how many days are left until an event). You do not
    know the current date or time on your own, so always use this tool instead
    of guessing.
    """
    current_datetime = datetime.now()
    return current_datetime.strftime("%A %d/%m/%Y %H:%M")


@tool(parse_docstring=True)
def days_between_dates(start_date: str, end_date: str) -> int:
    """Returns the number of days between two dates, as an integer.
    The result is positive if end_date is after start_date, and negative
    if it is before. Use it whenever the user asks how many days are left
    until a date or how many days have passed since a date. If one of the
    two dates is today, first call get_current_datetime to get the current
    date: never guess it.

    Args:
        start_date: The starting date, in the format DD/MM/YYYY (for example: 30/09/2026).
        end_date: The ending date, in the format DD/MM/YYYY (for example: 25/12/2026).
    """
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    difference = end - start
    return difference.days



agent = create_agent(
    model=model, 
    tools=[get_current_datetime, days_between_dates],
    system_prompt="You are a helpful assistant. When a question requires information you don't have, use the available tools instead of guessing. Always answer in Italian, clearly and concisely."
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Quanti giorni mancano a Natale?"}
        ]
    }
)

for message in result["messages"]:
    message.pretty_print()
