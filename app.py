import streamlit as st
import os
from dotenv import load_dotenv
from agent_logic import build_agent
from langchain_community.callbacks import StreamlitCallbackHandler # Importante per vedere i pensieri

load_dotenv()

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

st.title("✈️ Agente AI Travel Planner")
st.markdown("Modello: **Gemini 1.5 Flash** (Versione Stabile)")

if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra cronologia
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Es: Voglio andare a Roma in 2 per 5 giorni, 100 euro budget"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Contenitore per i pensieri dell'agente
        st_callback = StreamlitCallbackHandler(st.container())
        
        try:
            # Passiamo il callback per visualizzare i passaggi a schermo
            response = st.session_state.agent.invoke(
                {"input": prompt},
                {"callbacks": [st_callback]} 
            )
            output_text = response["output"]
            st.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            st.error(f"Errore: {e}")
            st.warning("Consiglio: Aspetta 1 minuto e riprova (limite API Google).")
