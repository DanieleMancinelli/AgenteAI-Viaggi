import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from tools_definition import travel_tools

load_dotenv()

def build_agent():
    # IL VINCITORE DELLA SCANSIONE
    model_name = "gemini-flash-lite-latest"
    
    print(f"--- Inizializzazione Agente con: {model_name} ---")
    
    llm = ChatGoogleGenerativeAI(
        model=model_name, 
        temperature=0,
        max_retries=1 # Se fallisce, stop. Non sprechiamo quota.
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True
    )

    # Prompt ottimizzato per il modello "Lite" (istruzioni più semplici e dirette)
    template = """
    Sei un assistente di viaggio.
    
    OBIETTIVO: Rispondere alla domanda dell'utente usando i tool se necessario.
    
    STRUMENTI A DISPOSIZIONE:
    {tools}
    
    NOMI STRUMENTI:
    {tool_names}
    
    ISTRUZIONI:
    1. Se hai bisogno di calcolare prezzi, usa calculate_budget.
    2. Se hai bisogno di info su una città, usa search_destinations.
    3. IMPORTANTE: Una volta usato il tool, dai SUBITO la "Final Answer".
    
    FORMATO (Usa esattamente questo):
    Question: la domanda
    Thought: devo usare un tool? (si/no)
    Action: nome_tool (o None)
    Action Input: input_tool
    Observation: risultato_tool
    Thought: ho l'info, rispondo.
    Final Answer: la risposta finale.

    Inizia ora:
    
    Question: {input}
    {chat_history}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template)

    agent = create_react_agent(llm, travel_tools, prompt)

    return AgentExecutor(
        agent=agent, 
        tools=travel_tools, 
        verbose=True, 
        memory=memory,
        handle_parsing_errors=True,
        max_iterations=3,      # Pochi passaggi per il modello Lite
        max_execution_time=30
    )
