import streamlit as st
import pandas as pd

# -----------------------------
# CONFIG UI
# -----------------------------
st.set_page_config(
    page_title="Fuel Manager",
    page_icon="⛽",
    layout="wide"
)

# -----------------------------
# CSS PER UI PIÙ BELLA
# -----------------------------
st.markdown("""
<style>
.big-title {
    font-size: 34px;
    font-weight: 700;
    color: #1f4e79;
}

.card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f4f6f8;
    margin-bottom: 10px;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.1);
}

.price {
    font-size: 26px;
    font-weight: bold;
    color: #00a86b;
}

.small {
    color: gray;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR MENU
# -----------------------------
menu = st.sidebar.selectbox(
    "📂 Menu",
    ["📊 Dashboard", "➕ Nuovo Cliente", "📋 Lista Clienti"]
)

# -----------------------------
# DATABASE MOCK (poi lo colleghi a Sheets)
# -----------------------------
if "clienti" not in st.session_state:
    st.session_state.clienti = pd.DataFrame([
        {"Nome": "Mario SRL", "PIVA": "123", "Telefono": "333111", "Margine": 0.05, "Trasporto": 0.02},
        {"Nome": "Luca Trasporti", "PIVA": "456", "Telefono": "333222", "Margine": 0.04, "Trasporto": 0.03},
    ])

if "prezzo_base" not in st.session_state:
    st.session_state.prezzo_base = 1.00

# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "📊 Dashboard":

    st.markdown('<div class="big-title">⛽ Fuel Dashboard</div>', unsafe_allow_html=True)

    prezzo_base = st.number_input(
        "💰 Prezzo base carburante",
        value=float(st.session_state.prezzo_base),
        step=0.01
    )

    st.session_state.prezzo_base = prezzo_base

    st.divider()

    st.subheader("👤 Clienti con prezzo aggiornato")

    for _, c in st.session_state.clienti.iterrows():

        prezzo_finale = prezzo_base + c["Margine"] + c["Trasporto"]

        msg = f"Carissimo {c['Nome']}, il prezzo di oggi è {prezzo_finale:.3f} €/L"

        wa_link = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"

        st.markdown(f"""
        <div class="card">
            <b>👤 {c['Nome']}</b><br>
            <span class="small">P.IVA: {c['PIVA']}</span><br><br>

            💰 Prezzo oggi:<br>
            <div class="price">{prezzo_finale:.3f} €/L</div><br>

            <a href="{wa_link}" target="_blank">
                <button style="
                    background-color:#25D366;
                    color:white;
                    border:none;
                    padding:10px 15px;
                    border-radius:8px;
                    cursor:pointer;
                ">
                📲 Invia WhatsApp
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# NUOVO CLIENTE
# -----------------------------
elif menu == "➕ Nuovo Cliente":

    st.subheader("➕ Inserisci nuovo cliente")

    nome = st.text_input("Nome cliente")
    piva = st.text_input("P.IVA")
    telefono = st.text_input("Telefono")
    margine = st.number_input("Margine", value=0.0, step=0.01)
    trasporto = st.number_input("Trasporto", value=0.0, step=0.01)

    if st.button("💾 Salva cliente"):
        nuovo = pd.DataFrame([{
            "Nome": nome,
            "PIVA": piva,
            "Telefono": telefono,
            "Margine": margine,
            "Trasporto": trasporto
        }])

        st.session_state.clienti = pd.concat([st.session_state.clienti, nuovo], ignore_index=True)

        st.success("Cliente salvato!")

# -----------------------------
# LISTA CLIENTI
# -----------------------------
elif menu == "📋 Lista Clienti":

    st.subheader("📋 Tutti i clienti")

    search = st.text_input("🔍 Cerca per Nome o P.IVA")

    df = st.session_state.clienti

    if search:
        df = df[
            df["Nome"].str.contains(search, case=False) |
            df["PIVA"].str.contains(search, case=False)
        ]

    st.dataframe(df, use_container_width=True)