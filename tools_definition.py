import os
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Strumento 1: Ricercatore di Destinazioni (Simulato)
@tool
def search_destinations(query: str) -> str:
    """
    Utile per trovare informazioni su destinazioni di viaggio.
    Input: Una stringa che descrive la città (es: "Tokyo").
    """
    data = {
        "tokyo": "Tokyo offre il tempio Senso-ji, Shibuya e ottimi ramen.",
        "parigi": "Parigi è famosa per la Torre Eiffel, il Louvre e i croissant.",
        "roma": "Roma offre il Colosseo, il Vaticano e la carbonara."
    }
    
    query_lower = query.lower()
    for city, info in data.items():
        if city in query_lower:
            return f"Info trovate: {info}"
    
    return "Nessuna info specifica trovata. Prova Tokyo, Parigi o Roma."

# Strumento 2: Calcolatore di Budget
@tool
def calculate_budget(inputs: str) -> str:
    """
    Calcola il costo totale.
    Input atteso: stringa 'costo_giornaliero, giorni, persone' (es: '100, 7, 2').
    """
    try:
        parts = [int(x.strip()) for x in inputs.split(",")]
        if len(parts) != 3:
            return "Errore: formatta come 'costo, giorni, persone'."
        
        daily, days, people = parts
        total = daily * days * people
        return f"Il costo totale stimato è: {total} EUR."
    except ValueError:
        return "Errore: usa solo numeri."

travel_tools = [search_destinations, calculate_budget]
