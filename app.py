import streamlit as st
import os
from dotenv import load_dotenv
from agent_logic import build_agent

load_dotenv()

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")
st.title("✈️ AI Agent: Planner Professionista")
st.markdown("Basato su **Groq (Llama 3)**")

# Inizializzazione sessione messaggi
if "messages" not in st.session_state:
    st.session_state.messages = []

# L'agente viene creato una volta sola
if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

# Visualizzazione chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Es: Voglio andare a Londra con 3 amici, amo la musica trap"):
    # 1. Aggiungi messaggio utente alla storia
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'agente sta pianificando..."):
            # 2. Costruisci il formato messaggi richiesto da LangGraph
            # Passiamo l'intera storia per mantenere la memoria (Planning State)
            history = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "assistant"
                history.append((role, m["content"]))
            
            try:
                # Chiamata all'agente con la storia completa
                response = st.session_state.agent.invoke({"messages": history})
                
                # Prendi l'ultimo messaggio (la risposta finale dell'agente)
                final_answer = response["messages"][-1].content
                
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            except Exception as e:
                st.error(f"Errore tecnico: {e}")
