import streamlit as st

# 1. Configurazione della pagina con titolo ed emoji italiana
st.set_page_config(
    page_title="Il Grande Quiz d'Italia",
    page_icon="🇮🇹",
    layout="centered"
)

# 2. Stile CSS personalizzato (Tricolore e dettagli italiani)
st.markdown("""
    <style>
    .main {
        background-color: #fdfbf7;
    }
    h1 {
        color: #009246; /* Verde Italia */
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h2, h3 {
        color: #ce2b37; /* Rosso Italia */
    }
    .stButton>button {
        background-color: #009246;
        color: white;
        border-radius: 20px;
        border: 2px solid #ce2b37;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ce2b37;
        color: white;
        border-color: #009246;
    }
    .sidebar .sidebar-content {
        background-color: #f1f2f1;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Database delle domande suddivise per livelli
QUIZ_DATA = {
    "Livello 1: Espresso ☕ (Principiante)": [
        {
            "quest": "Come si dice 'Hello' in italiano in modo informale?",
            "options": ["Arrivederci", "Ciao", "Prego", "Grazie"],
            "correct": "Ciao"
        },
        {
            "quest": "Qual è l'articolo determinativo plurale corretto per 'ragazzi'?",
            "options": ["Il", "Lo", "I", "Gli"],
            "correct": "I"
        },
        {
            "quest": "Completa la frase: 'Un cappuccino, per ____, grazie.'",
            "options": ["favore", "piacere", "scusa", "prego"],
            "correct": "favore"
        }
    ],
    "Livello 2: Aperitivo 🍹 (Intermedio)": [
        {
            "quest": "Qual è il passato prossimo corretto del verbo andare per una donna? 'Ieri io...'",
            "options": ["ho andato", "sono andato", "sono andata", "ho andata"],
            "correct": "sono andata"
        },
        {
            "quest": "Cosa significa l'espressione tipica 'In bocca al lupo'?",
            "options": ["Buona fortuna", "Ho fame", "Attento al cane", "Buonanotte"],
            "correct": "Buona fortuna"
        },
        {
            "quest": "Quale di queste parole è un sinonimo di 'veloce'?",
            "options": ["Lento", "Rapido", "Calmo", "Pesante"],
            "correct": "Rapido"
        }
    ],
    "Livello 3: Dolce Vita 🎭 (Avanzato)": [
        {
            "quest": "Scegli la frase corretta con il congiuntivo:",
            "options": [
                "Penso che tu hai ragione.",
                "Penso che tu abbia ragione.",
                "Penso che tu avessi ragione.",
                "Penso che tu avrai ragione."
            ],
            "correct": "Penso che tu abbia ragione."
        },
        {
            "quest": "Completa il periodo ipotetico della irrealtà: 'Se avessi studiato di più,...'",
            "options": [
                "superavo l'esame.",
                "avrei superato l'esame.",
                "avessi superato l'esame.",
                "supererò l'esame."
            ],
            "correct": "avrei superato l'esame."
        }
    ]
}

# SOGLIA PER SBLOCCARE IL LIVELLO SUCCESSIVO (es. servono almeno 2 risposte corrette)
SOGLIA_SBLOCCO = 2

# 4. Inizializzazione dello Stato della Sessione (Session State)
if "unlocked_levels" not in st.session_state:
    st.session_state.unlocked_levels = ["Livello 1: Espresso ☕ (Principiante)"]
if "current_level" not in st.session_state:
    st.session_state.current_level = "Livello 1: Espresso ☕ (Principiante)"
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# Funzione per resettare lo stato quando si cambia livello manualmente
def cambia_livello(nuovo_livello):
    st.session_state.current_level = nuovo_livello
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_option = None

# 5. Interfaccia della Barra Laterale (Sidebar)
st.sidebar.title("🇮🇹 Menu del Quiz")
st.sidebar.write("Sblocca i livelli rispondendo correttamente alle domande!")

# Bottoni nella sidebar per navigare tra i livelli sbloccati
for lvl in QUIZ_DATA.keys():
    if lvl in st.session_state.unlocked_levels:
        if st.sidebar.button(f"🔓 {lvl}", key=f"btn_{lvl}"):
            cambia_livello(lvl)
    else:
        st.sidebar.button(f"🔒 {lvl} (Bloccato)", disabled=True, key=f"btn_{lvl}")

# Bottoncino di reset totale
st.sidebar.markdown("---")
if st.sidebar.button("Ricomincia da capo 🔄"):
    st.session_state.unlocked_levels = ["Livello 1: Espresso ☕ (Principiante)"]
    cambia_livello("Livello 1: Espresso ☕ (Principiante)")
    st.rerun()

# 6. Contenuto Principale
st.title("Benvenuti al Quiz di Italiano! 🍝")
st.write(f"Stai giocando a: **{st.session_state.current_level}**")

domande_attuali = QUIZ_DATA[st.session_state.current_level]
totale_domande = len(domande_attuali)

# Controllo se il livello corrente è completato
if st.session_state.q_index < totale_domande:
    domanda_corrente = domande_attuali[st.session_state.q_index]
    
    st.write(f"### Domanda {st.session_state.q_index + 1} di {totale_domande}")
    st.write(domanda_corrente["quest"])
    
    # Radio button per le opzioni
    scelta = st.radio(
        "Seleziona la risposta corretta:",
        domanda_corrente["options"],
        index=None if not st.session_state.answered else domanda_corrente["options"].index(st.session_state.selected_option),
        disabled=st.session_state.answered,
        key=f"radio_{st.session_state.current_level}_{st.session_state.q_index}"
    )
    
    # Bottone per confermare la risposta
    if not st.session_state.answered:
        if st.button("Verifica la risposta 🍕"):
            if scelta is None:
                st.warning("Per favore, seleziona una risposta prima di continuare!")
            else:
                st.session_state.answered = True
                st.session_state.selected_option = scelta
                if scelta == domanda_corrente["correct"]:
                    st.success("Bravissimo! Risposta Esatta! 🟢")
                    st.session_state.score += 1
                else:
                    st.error(f"Sbagliato! 🔴 La risposta corretta era: {domanda_corrente['correct']}")
                st.rerun()
                
    # Bottone per andare avanti dopo la verifica
    else:
        if st.button("Prossima domanda ➡️"):
            st.session_state.q_index += 1
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

else:
    # Fine del livello attuale
    st.balloons()
    st.write("### 🎉 Livello Completato!")
    st.write(f"Hai totalizzato: **{st.session_state.score} punti su {totale_domande}**")
    
    # Logica di sblocco livello successivo
    lista_livelli = list(QUIZ_DATA.keys())
    indice_attuale = lista_livelli.index(st.session_state.current_level)
    
    if st.session_state.score >= SOGLIA_SBLOCCO:
        if indice_attuale + 1 < len(lista_livelli):
            prossimo_livello = lista_livelli[indice_attuale + 1]
            
            if prossimo_livello not in st.session_state.unlocked_levels:
                st.session_state.unlocked_levels.append(prossimo_livello)
                st.success(f"🥳 Complimenti! Hai sbloccato il livello successivo: **{prossimo_livello}**!")
            
            if st.button(f"Vai al {prossimo_livello} 🚀"):
                cambia_livello(prossimo_livello)
                st.rerun()
        else:
            st.success("🏆 Bravissimo! Hai completato tutti i livelli del quiz! Sei un vero esperto della lingua italiana! 🇮🇹")
    else:
        st.warning(f"Non hai raggiunto il punteggio minimo ({SOGLIA_SBLOCCO} risposte esatte) per sbloccare il prossimo livello.")
        if st.button("Riprova questo livello 🔄"):
            cambia_livello(st.session_state.current_level)
            st.rerun()
