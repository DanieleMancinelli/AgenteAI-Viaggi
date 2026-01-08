import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Lista dei candidati probabili
candidates = [
    "gemini-1.5-flash-latest",
    "gemini-pro-latest",
    "gemini-2.0-flash-exp",
    "gemini-1.5-pro-latest"
]

print("--- INIZIO TEST CONNESSIONE ---")

working_model = None

for model_name in candidates:
    print(f"\nTentativo con: {model_name}...", end=" ")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Ciao")
        print(f"✅ SUCCESSO!")
        print(f"Risposta ricevuta: {response.text.strip()[:20]}...")
        working_model = model_name
        break # Trovato! Ci fermiamo al primo che funziona
    except Exception as e:
        print("❌ FALLITO")
        if "404" in str(e):
            print("   Motivo: Modello non trovato o nome errato.")
        elif "429" in str(e):
            print("   Motivo: Quota esaurita (Troppe richieste).")
        else:
            print(f"   Errore: {str(e)[:100]}")

print("\n--------------------------------")
if working_model:
    print(f"🏆 VINCITORE: Usa '{working_model}' nel tuo codice.")
else:
    print("�� NESSUN MODELLO FUNZIONANTE. Devi attendere qualche minuto per il reset della quota.")
