import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel Manager", layout="wide")

# -----------------------
# INIT SAFE STATE
# -----------------------
if "clienti" not in st.session_state:
    st.session_state.clienti = pd.DataFrame([
        {"ID": 1, "Nome": "Mario SRL", "PIVA": "123", "Telefono": "333111", "Margine": 0.025, "Trasporto": 0.01},
        {"ID": 2, "Nome": "Luca Trasporti", "PIVA": "456", "Telefono": "333222", "Margine": 0.03, "Trasporto": 0.02},
    ])

if "prezzo_base" not in st.session_state:
    st.session_state.prezzo_base = 1.00

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# -----------------------
# SAFE NAVIGATION
# -----------------------
def go(page_name):
    st.session_state.page = page_name
    st.session_state.edit_id = None

# -----------------------
# MENU (BUTTON STYLE)
# -----------------------
st.title("⛽ Fuel Manager")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Dashboard"):
        go("dashboard")

with col2:
    if st.button("➕ Nuovo Cliente"):
        go("add")

with col3:
    if st.button("📋 Clienti"):
        go("list")

page = st.session_state.page

# -----------------------
# DASHBOARD
# -----------------------
if page == "dashboard":

    st.subheader("📊 Dashboard")

    search = st.text_input("🔍 Cerca cliente")

    prezzo_base = st.number_input(
        "💰 Prezzo base",
        value=float(st.session_state.prezzo_base),
        step=0.001,
        format="%.3f"
    )

    st.session_state.prezzo_base = prezzo_base

    df = st.session_state.clienti

    if search:
        df = df[
            df["Nome"].str.contains(search, case=False) |
            df["PIVA"].str.contains(search, case=False)
        ]

    for _, c in df.iterrows():

        prezzo_finale = prezzo_base + c["Margine"] + c["Trasporto"]

        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.markdown(f"### 👤 {c['Nome']}")
            st.caption(f"P.IVA: {c['PIVA']}")

        with col2:
            st.metric("💰", f"{prezzo_finale:.3f} €/L")

        with col3:
            msg = f"Carissimo {c['Nome']}, prezzo oggi {prezzo_finale:.3f} €/L"
            wa = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"
            st.link_button("📲 WhatsApp", wa)

        with col4:
            if st.button("🗑️", key=f"del_{c['ID']}"):
                st.session_state.clienti = st.session_state.clienti[
                    st.session_state.clienti["ID"] != c["ID"]
                ]
                st.rerun()

            if st.button("✏️", key=f"edit_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                go("add")

# -----------------------
# ADD / EDIT CLIENTE
# -----------------------
elif page == "add":

    st.subheader("➕ Cliente")

    editing = st.session_state.edit_id is not None

    if editing:
        df_edit = st.session_state.clienti[
            st.session_state.clienti["ID"] == st.session_state.edit_id
        ]

        if df_edit.empty:
            st.error("Cliente non trovato")
            st.stop()

        cliente = df_edit.iloc[0]
    else:
        cliente = {"Nome": "", "PIVA": "", "Telefono": "", "Margine": 0.0, "Trasporto": 0.0}

    nome = st.text_input("Nome", value=cliente["Nome"])
    piva = st.text_input("P.IVA", value=cliente["PIVA"])
    tel = st.text_input("Telefono", value=cliente["Telefono"])
    margine = st.number_input("Margine", value=float(cliente["Margine"]), step=0.001, format="%.3f")
    trasporto = st.number_input("Trasporto", value=float(cliente["Trasporto"]), step=0.001, format="%.3f")

    if st.button("💾 Salva"):

        if editing:
            st.session_state.clienti.loc[
                st.session_state.clienti["ID"] == st.session_state.edit_id,
                ["Nome", "PIVA", "Telefono", "Margine", "Trasporto"]
            ] = [nome, piva, tel, margine, trasporto]

            st.session_state.edit_id = None

        else:
            new_id = int(st.session_state.clienti["ID"].max()) + 1

            new_row = pd.DataFrame([{
                "ID": new_id,
                "Nome": nome,
                "PIVA": piva,
                "Telefono": tel,
                "Margine": margine,
                "Trasporto": trasporto
            }])

            st.session_state.clienti = pd.concat([st.session_state.clienti, new_row], ignore_index=True)

        st.success("Salvato!")
        go("dashboard")

# -----------------------
# LISTA CLIENTI
# -----------------------
elif page == "list":

    st.subheader("📋 Clienti")

    st.dataframe(st.session_state.clienti, use_container_width=True)
