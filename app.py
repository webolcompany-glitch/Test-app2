import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fuel Manager",
    page_icon="⛽",
    layout="wide"
)

# -----------------------
# SESSION DATA
# -----------------------
if "clienti" not in st.session_state:
    st.session_state.clienti = pd.DataFrame([
        {"Nome": "Mario SRL", "PIVA": "123", "Telefono": "333111", "Margine": 0.05, "Trasporto": 0.02},
        {"Nome": "Luca Trasporti", "PIVA": "456", "Telefono": "333222", "Margine": 0.04, "Trasporto": 0.03},
    ])

if "prezzo_base" not in st.session_state:
    st.session_state.prezzo_base = 1.00

# -----------------------
# MENU SIDEBAR
# -----------------------
menu = st.sidebar.selectbox(
    "📂 Menu",
    ["📊 Dashboard", "➕ Nuovo Cliente", "📋 Lista Clienti"]
)

# -----------------------
# DASHBOARD
# -----------------------
if menu == "📊 Dashboard":

    st.title("⛽ Dashboard")

    prezzo_base = st.number_input(
        "💰 Prezzo base oggi",
        value=float(st.session_state.prezzo_base),
        step=0.01
    )

    st.session_state.prezzo_base = prezzo_base

    st.divider()

    for i, row in st.session_state.clienti.iterrows():

        prezzo_finale = prezzo_base + row["Margine"] + row["Trasporto"]

        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
            st.subheader(f"👤 {row['Nome']}")
            st.caption(f"P.IVA: {row['PIVA']}")

        with col2:
            st.metric("💰 Prezzo", f"{prezzo_finale:.3f} €/L")

        with col3:
            msg = f"Carissimo {row['Nome']}, il prezzo di oggi è {prezzo_finale:.3f} €/L"
            wa_link = f"https://wa.me/{row['Telefono']}?text={msg.replace(' ', '%20')}"

            st.link_button("📲 WhatsApp", wa_link)

        st.divider()

# -----------------------
# NUOVO CLIENTE
# -----------------------
elif menu == "➕ Nuovo Cliente":

    st.title("➕ Inserisci Cliente")

    nome = st.text_input("Nome")
    piva = st.text_input("P.IVA")
    telefono = st.text_input("Telefono")
    margine = st.number_input("Margine", value=0.0, step=0.01)
    trasporto = st.number_input("Trasporto", value=0.0, step=0.01)

    if st.button("💾 Salva"):

        nuovo = pd.DataFrame([{
            "Nome": nome,
            "PIVA": piva,
            "Telefono": telefono,
            "Margine": margine,
            "Trasporto": trasporto
        }])

        st.session_state.clienti = pd.concat([st.session_state.clienti, nuovo], ignore_index=True)

        st.success("Cliente aggiunto!")

# -----------------------
# LISTA CLIENTI + RICERCA
# -----------------------
elif menu == "📋 Lista Clienti":

    st.title("📋 Clienti")

    search = st.text_input("🔍 Cerca per Nome o P.IVA")

    df = st.session_state.clienti

    if search:
        df = df[
            df["Nome"].str.contains(search, case=False) |
            df["PIVA"].str.contains(search, case=False)
        ]

    st.dataframe(df, use_container_width=True)
