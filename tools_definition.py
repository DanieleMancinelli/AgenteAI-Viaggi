import os
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

search = DuckDuckGoSearchRun()

@tool
def web_search_tool(query: str) -> str:
    """Cerca su internet. AGGIUNGE AUTOMATICAMENTE '2026' alla ricerca per evitare dati vecchi."""
    current_year = "2026"
    return search.run(f"{query} {current_year} events clubs")

@tool
def calculate_budget(inputs: str) -> str:
    """
    Calcola il budget. 
    FORMATO: 'euro_giornalieri_per_persona, giorni, persone' 
    Esempio: se il budget totale è 2000 per 4 persone in 5 giorni, 
    fai 2000 / 4 / 5 = 100. Passa '100, 5, 4'.
    """
    try:
        p = [float(x.strip()) for x in inputs.split(",")]
        total = p[0] * p[1] * p[2]
        return f"Il costo totale per {int(p[2])} persone per {int(p[1])} giorni è {total} EUR."
    except:
        return "Errore: inserisci 'euro_giornalieri, giorni, persone'."

travel_tools = [web_search_tool, calculate_budget]
