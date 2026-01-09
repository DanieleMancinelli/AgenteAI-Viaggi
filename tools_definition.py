import os
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()

search = DuckDuckGoSearchRun()

@tool
def web_search_tool(query: str) -> str:
    """Cerca informazioni reali e aggiornate su internet."""
    return search.run(query)

@tool
def calculate_budget(inputs: str) -> str:
    """Calcola il budget. Input: 'euro_giorno, giorni, persone'"""
    try:
        parts = [int(x.strip()) for x in inputs.split(",")]
        total = parts[0] * parts[1] * parts[2]
        return f"Budget totale stimato: {total} EUR."
    except:
        return "Errore: servono numeri separati da virgola."

travel_tools = [web_search_tool, calculate_budget]
