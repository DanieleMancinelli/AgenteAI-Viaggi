import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.memory import ConversationBufferMemory
from tools_definition import travel_tools

load_dotenv()

def build_agent():
    # Usiamo Llama 3 70B: ha una logica di planning superiore
    llm = ChatGroq(
        temperature=0, 
        model_name="llama3-70b-8192", 
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # Memory caricata correttamente da community
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    template = """Sei un Travel Planner esperto e proattivo. 
Segui rigorosamente questo PROTOCOLLO DI PLANNING (Capitolo 6 Chip Huyen):

1. FASE DI INTERVISTA: Per creare un piano ho bisogno di:
   - DESTINAZIONE
   - GIORNI DI PERMANENZA
   - BUDGET GIORNALIERO A TESTA
   
2. VALUTAZIONE:
   - Se l'utente non fornisce questi 3 dati, NON cercare su internet e NON calcolare budget. 
   - Rispondi ringraziando per i dettagli forniti (es. i gusti trap) e chiedi esplicitamente cosa manca.
   
3. AZIONE:
   - Solo quando hai TUTTO, usa 'web_search_tool' per cercare club/eventi reali e 'calculate_budget' per il costo totale.

STRUMENTI:
{tools}

FORMATO OBBLIGATORIO:
Question: {input}
Thought: Ho Destinazione, Giorni e Budget? Se no, devo chiedere. Se sì, agisco.
Action: uno tra [{tool_names}] (SOLO se hai tutti i dati)
Action Input: input del tool
Observation: risultato
... (ripeti Thought/Action se necessario)
Thought: Ora posso rispondere.
Final Answer: la risposta finale all'utente.

STORIA CHAT:
{chat_history}

RAGIONAMENTO AGENTE:
Thought: {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, travel_tools, prompt)

    return AgentExecutor(
        agent=agent, 
        tools=travel_tools, 
        memory=memory, 
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
