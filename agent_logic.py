import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from tools_definition import travel_tools

load_dotenv()

def build_agent():
    model_name = "gemini-flash-lite-latest"
    
    llm = ChatGoogleGenerativeAI(
        model=model_name, 
        temperature=0,
        max_retries=1
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True
    )

    template = """
    Sei un assistente automatico che esegue comandi precisi.
    
    STRUMENTI:
    {tools}
    
    NOMI STRUMENTI:
    {tool_names}
    
    PROTOCOLLO DI SICUREZZA (DA RISPETTARE SEMPRE):
    1. NON chiamare mai lo stesso tool due volte con lo stesso input.
    2. Se l'Osservazione (Observation) contiene "Nessuna informazione" o "ISTRUZIONE PER L'AGENTE", DEVI FERMARTI IMMEDIATAMENTE.
    3. La tua prossima mossa DEVE essere "Final Answer" copiando il messaggio di errore.
    
    FORMATO RIGIDO:
    Question: la domanda
    Thought: Cosa devo fare?
    Action: {tool_names} (o None)
    Action Input: input
    Observation: risultato
    Thought: Ho finito? Se l'osservazione è negativa, dico di no.
    Final Answer: Risposta finale.

    ESEMPIO DI ARRESTO:
    Question: Londra
    Thought: Cerco Londra
    Action: search_destinations
    Action Input: Londra
    Observation: RISULTATO: Nessuna informazione...
    Thought: Il tool ha fallito. Mi fermo.
    Final Answer: Non ho informazioni su Londra.

    Inizia il task:
    
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
        # Se l'agente impazzisce e sbaglia formato, gli forziamo questa risposta invece di riprovare
        handle_parsing_errors="Ho avuto un problema tecnico, ma la risposta è: controlla i dati inseriti o prova un'altra destinazione.",
        max_iterations=3, 
        max_execution_time=15 # Timeout cortissimo: se non rispondi in 15 secondi, ti stacco.
    )
