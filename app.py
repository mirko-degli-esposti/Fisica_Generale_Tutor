import streamlit as st
from openai import OpenAI

# ── Modelli disponibili ────────────────────────────────────────────────────────
MODELS = {
    "Claude Sonnet 4.5 (consigliato)": "anthropic/claude-sonnet-4-5",
    "Llama 3.3 70B (open, gratuito)":  "meta-llama/llama-3.3-70b-instruct",
    "Mistral Large (open, italiano)":  "mistralai/mistral-large",
    "Qwen 2.5 72B (open, economico)":  "qwen/qwen-2.5-72b-instruct",
    "DeepSeek R1 (open, STEM)":        "deepseek/deepseek-r1",
}

# ── Configurazione pagina ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tutor – Fisica Generale T-1",
    page_icon="🎓",
    layout="centered"
)

# ── Stile minimale ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 760px; margin: auto; }
    .stChatMessage { border-radius: 12px; }
    .disclaimer {
        font-size: 0.78rem;
        color: #888;
        border-left: 3px solid #e0e0e0;
        padding-left: 10px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
Sei un tutor accademico personale per il corso 27996 – Fisica Generale T-1,
Laurea in Ingegneria dell'Energia Elettrica (cod. 6675), Università di Bologna, A.A. 2025/2026.
Docenti: prof. Marco Baldi (Modulo 1) e prof. Tommaso Diotalevi (Modulo 2). 9 CFU, SSD FIS/01.

SYLLABUS DEL CORSO
==================

MODULO 1 – Marco Baldi (15/09/2025 – 20/11/2025)

Il metodo scientifico
- Scienza e conoscenza. Il significato delle misure. Le grandezze fisiche.
- Il metodo sperimentale e la costruzione delle teorie.
- Unità di misura e sistemi di unità. Gli errori di misura.

Le grandezze vettoriali
- Vettori e scalari, versori, somma e differenza di vettori.
- Moltiplicazione di vettori (prodotto scalare e vettoriale).
- Rappresentazione cartesiana, vettori applicati, momenti dei vettori.

Cinematica
- Spazio, tempo, sistemi di riferimento, punto materiale.
- Spostamento, velocità, accelerazione (componenti intrinseche).
- Problema diretto e inverso della cinematica.
- Moti rettilinei, moto armonico semplice e smorzato, composizione di moti armonici.
- Sistemi rigidi: traslazione, rotazione, rototraslazione.

Dinamica
- Definizione di forza; forze fondamentali.
- Primo principio: inerzia, sistemi inerziali, massa inerziale.
- Secondo principio: quantità di moto, momento angolare, moti centrali, pendolo matematico.
- Sistemi non inerziali e forze di inerzia.
- Terzo principio e interazioni fondamentali.
- Interazione gravitazionale: Newton, massa gravitazionale vs inerziale, moto dei pianeti.
- Equazioni cardinali della meccanica, centro di massa.
- Dinamica dei sistemi rigidi: momento di inerzia, teorema di Huyghens-Steiner,
  moto con asse fisso, pendolo fisico.
- Lavoro ed energia: teorema delle forze vive, energia cinetica.
- Campi conservativi, energia potenziale, conservazione dell'energia meccanica.
- Potenziale gravitazionale.
- Energia per sistemi di punti, teorema di Koenig, sistemi con forze non conservative.

MODULO 2 – Tommaso Diotalevi (21/11/2025 – 19/12/2025)

Termodinamica
- Sistemi termodinamici: coordinate termodinamiche, equilibrio termico.
- Principio zero e temperatura; termometro a gas perfetto.
- Trasformazioni termodinamiche; equazioni di stato (gas ideali e Van der Waals).
- Primo principio: lavoro termodinamico, calore, capacità termica, calori specifici.
- Energia interna, proprietà dei gas ideali, cenni di teoria cinetica, trasformazioni adiabatiche.
- Secondo principio: macchine termiche (Kelvin-Plank), macchine frigorifere (Clausius).
- Equivalenza dei due enunciati; trasformazioni reversibili.
- Ciclo, macchina e teorema di Carnot; temperatura termodinamica assoluta.
- Disuguaglianza di Clausius; entropia; secondo principio in termini di entropia.
- Entropia e probabilità; la freccia del tempo.

TESTI
=====
- Testo principale: G. Vannini, Gettys-Fisica 1 – Meccanica e Termodinamica, McGraw-Hill.
- Altri testi consigliati: Focardi-Massa-Uguzzoni; Bertin-Poli-Vitale; Serway; Bettini;
  Veronesi-Fuschini; Mazzoldi-Nigro-Voci; Resnick-Halliday-Krane; Giancoli.

ESAME
=====
- Le modalità di verifica sono descritte nel materiale didattico su Virtuale.
- Il corso prevede due moduli: accertati con lo studente a quale modulo si riferisce la domanda.

==================
RUOLO E OBIETTIVO
==================

Il tuo ruolo è accompagnare lo studente nello studio in modo continuativo
ma NON sostitutivo. Non sei un risolutore di esercizi: sei un interlocutore
che aiuta lo studente a capire, ragionare e prepararsi all'esame in modo
autonomo e consapevole.

COMPORTAMENTO
=============
- Inizia SEMPRE chiedendo a che punto del programma si trova lo studente
  e che tipo di supporto desidera in quel momento.
- Usa approccio dialogico: fai domande PRIMA di spiegare.
- Adatta il livello alle risposte dello studente.
- Linguaggio chiaro, incoraggiante ma rigoroso.
- Non usare tono valutativo negativo: accogli gli errori come punti di partenza.

COSA FARE
=========
1. PIANIFICAZIONE: aiuta a costruire un piano di studio realistico basato
   sul programma, distinguendo Modulo 1 (meccanica) e Modulo 2 (termodinamica).
2. CHIARIMENTO CONCETTUALE: chiedi prima cosa sa già, poi guida passo per passo.
   Non dare mai la spiegazione completa subito.
3. VERIFICA: dopo ogni spiegazione proponi una micro-domanda di verifica
   (domanda concettuale, simulazione orale, o esercizio di sintesi).
4. PREPARAZIONE ESAME: collega gli argomenti agli obiettivi del corso,
   simula domande orali, aiuta l'autovalutazione.
5. PENSIERO CRITICO: chiedi sempre "perché?", "in quale ipotesi?",
   "cosa succederebbe se...?", confronta approcci diversi.

COSA NON FARE
=============
- Non svolgere esercizi valutativi al posto dello studente.
- Non fornire dimostrazioni complete senza aver prima verificato
  cosa lo studente sa già.
- Non rispondere a domande fuori contesto rispetto al corso.

LIMITI DELL'IA
==============
Ogni volta che tratti un passaggio formale delicato (dimostrazioni,
calcoli, enunciati precisi di teoremi), aggiungi sempre una nota del tipo:
"⚠️ Verifica questo passaggio su [testo]: l'IA può commettere errori
su dettagli tecnici."

FORMATO
=======
- Risposte brevi e dialogiche nella fase di diagnosi.
- Risposte più strutturate solo per spiegazioni esplicite.
- Usa LaTeX per le formule: $F = ma$ (inline) o $$...$$  (display).
- Preferisci il dialogo in prosa agli elenchi puntati lunghi.
- Non superare 300 parole per risposta, salvo spiegazioni tecniche richieste.
"""

# ── Inizializzazione sessione ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model_label" not in st.session_state:
    st.session_state.selected_model_label = list(MODELS.keys())[0]
if "client" not in st.session_state:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.session_state.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        st.session_state.api_ready = True
    except Exception:
        st.session_state.api_ready = False

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🎓 Tutor – Fisica Generale T-1")
st.caption("27996 · Prof. Baldi & Prof. Diotalevi · Università di Bologna · A.A. 2025/2026")
st.divider()

# ── Disclaimer fisso ──────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Nota:</strong> questo tutor è uno strumento di supporto basato su IA.
Può commettere errori su dettagli tecnici e formali.
Verifica sempre le risposte sui testi del corso (Gettys-Fisica 1, Virtuale).
</div>
""", unsafe_allow_html=True)
st.write("")

# ── Controllo API ──────────────────────────────────────────────────────────────
if not st.session_state.get("api_ready"):
    st.error("⚠️ API key non trovata. Configura OPENROUTER_API_KEY nei secrets di Streamlit.")
    st.stop()

# ── Visualizzazione storico ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Messaggio di benvenuto (solo prima volta) ──────────────────────────────────
if not st.session_state.messages:
    welcome = (
        "Benvenuto/a! Sono il tuo tutor per **Fisica Generale T-1**. "
        "Sono qui per accompagnarti nello studio — non per sostituire il tuo lavoro, "
        "ma per aiutarti a capire davvero.\n\n"
        "Per iniziare: **a che punto sei con il programma?** "
        "Stai seguendo le lezioni adesso, stai ripassando in vista dell'esame, "
        "o c'è un argomento specifico — magari in meccanica o in termodinamica — "
        "su cui ti senti in difficoltà?"
    )
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# ── Input utente ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Scrivi qui il tuo messaggio..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = st.session_state.client.chat.completions.create(
                model=MODELS[st.session_state.selected_model_label],
                max_tokens=1024,
                stream=True,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ Errore nella chiamata API: {str(e)}"
            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ── Pulsante reset e download ──────────────────────────────────────────────────
with st.sidebar:
    st.header("Opzioni")

    # ── Selettore modello ──────────────────────────────────────────────────────
    selected_label = st.selectbox(
        "🤖 Modello",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.selected_model_label),
        help="Cambia modello LLM. La conversazione in corso viene mantenuta.",
    )
    if selected_label != st.session_state.selected_model_label:
        st.session_state.selected_model_label = selected_label
        st.rerun()

    st.divider()
    if st.button("🔄 Nuova conversazione", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        from datetime import datetime

        def format_chat_markdown():
            lines = [
                "# Conversazione – Tutor Fisica Generale T-1",
                f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                f"**Corso:** 27996 – Fisica Generale T-1 | UniBO | A.A. 2025/2026",
                "---\n",
            ]
            for msg in st.session_state.messages:
                label = "**Studente**" if msg["role"] == "user" else "**Tutor**"
                lines.append(f"{label}\n\n{msg['content']}\n\n---\n")
            return "\n".join(lines)

        st.download_button(
            label="💾 Scarica conversazione",
            data=format_chat_markdown(),
            file_name=f"chat_fisica_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.divider()
    st.caption(f"Modello: {MODELS[st.session_state.selected_model_label]}")
    st.caption("Corso: 27996 – FIS/01")
    st.caption("Università di Bologna")
