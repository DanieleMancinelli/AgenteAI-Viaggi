import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("ERRORE: Chiave API non trovata nel file .env")
    exit()

genai.configure(api_key=api_key)

print("--- INIZIO SCANSIONE DI SOPRAVVIVENZA ---")
print("Cerco un modello che risponda senza errori 404 o 429...\n")

found_model = None

# Ottieni la lista reale dal server Google
all_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

# Ordiniamo per provare prima quelli che di solito sono free (Flash, Pro standard)
# Mettiamo in fondo quelli sperimentali (Exp, Preview) che spesso danno problemi
priority_models = sorted(all_models, key=lambda x: ("flash" not in x.name, "exp" in x.name))

for m in priority_models:
    model_name = m.name # es: models/gemini-1.5-flash
    clean_name = model_name.replace("models/", "") # langchain vuole il nome pulito
    
    print(f"Testando: {clean_name:<30}", end=" -> ")
    
    try:
        model = genai.GenerativeModel(model_name)
        # Proviamo a generare 1 token
        response = model.generate_content("X")
        print("✅ SUCCESSO! FUNZIONA!")
        found_model = clean_name
        break # Trovato! Usciamo subito
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            if "limit: 0" in error_msg:
                print("❌ Accesso Negato (Limit: 0)")
            else:
                print("⚠️ Quota Momentaneamente Piena (Riprova tra poco)")
                # Se è solo piena ma il limite non è 0, potrebbe essere un buon candidato, ma continuiamo a cercare
        elif "404" in error_msg:
            print("❌ Non Trovato")
        else:
            print(f"❌ Errore: {error_msg[:20]}...")

print("\n" + "="*40)
if found_model:
    print(f"🏆 IL VINCITORE È: {found_model}")
    print(f"Usa questo nome ESATTO nel tuo codice.")
else:
    print("😭 Nessun modello accessibile trovato.")
print("="*40)
