import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools_definition import travel_tools

load_dotenv()

def build_agent():
    llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

    # ISTRUZIONI AVANZATE (Planning, Date Awareness, Reasoning)
    instructions = """Sei un Travel Planner AI di alto livello. 
DATA CORRENTE: Gennaio 2026.

PROTOCOLLO DI PIANIFICAZIONE:
1. PARSING INTELLIGENTE: Se l'utente dice 'ho un budget di 2000 euro' per 5 giorni e 4 persone, capisci che è il TOTALE. Dividilo tu (2000/5/4 = 100€ al giorno) prima di usare il tool.
2. VERIFICA TEMPORALE: Ignora ogni evento o data nel passato (2024/2025). Cerca solo eventi nel 2026.
3. RAGIONAMENTO (REACTION): Prima di rispondere, chiediti: 'Questa cifra di 40.000€ ha senso per un viaggio di 5 giorni?'. Se la risposta è no, correggi il calcolo.

REGOLE TOOL:
- Se mancano i giorni o il budget pro-capite, FERMATI e chiedi.
- Usa 'web_search_tool' specificando 'London trap clubs schedule 2026'.

Sii preciso, non dare informazioni obsolete."""

    return create_react_agent(llm, travel_tools, prompt=instructions)
