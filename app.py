import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel SaaS", layout="wide")

# -----------------------
# INIT DATA
# -----------------------
if "clienti" not in st.session_state:
    st.session_state.clienti = pd.DataFrame([
        {"ID": 1, "Nome": "Mario SRL", "PIVA": "123", "Telefono": "333111", "Margine": 0.025, "Trasporto": 0.01},
        {"ID": 2, "Nome": "Luca Trasporti", "PIVA": "456", "Telefono": "333222", "Margine": 0.03, "Trasporto": 0.02},
    ])

if "prezzo_base" not in st.session_state:
    st.session_state.prezzo_base = 1.000

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# -----------------------
# SIDEBAR MENU
# -----------------------
page = st.sidebar.radio(
    "📂 MENU",
    ["📊 Dashboard", "➕ Nuovo Cliente"]
)

# -----------------------
# DASHBOARD
# -----------------------
if page == "📊 Dashboard":

    st.title("⛽ Fuel SaaS Dashboard")

    df = st.session_state.clienti

    # -----------------------
    # KPI CALC
    # -----------------------
    prezzo_base = st.number_input(
        "💰 Prezzo base oggi",
        value=float(st.session_state.prezzo_base),
        step=0.001,
        format="%.3f"
    )

    st.session_state.prezzo_base = prezzo_base

    media_margine = df["Margine"].mean()
    clienti_count = len(df)

    prezzo_medio = (prezzo_base + df["Margine"] + df["Trasporto"]).mean()

    # -----------------------
    # KPI CARDS (TOP)
    # -----------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Prezzo base", f"{prezzo_base:.3f} €")
    col2.metric("👤 Clienti", clienti_count)
    col3.metric("📊 Margine medio", f"{media_margine:.3f}")
    col4.metric("⛽ Prezzo medio", f"{prezzo_medio:.3f}")

    st.divider()

    # -----------------------
    # SEARCH
    # -----------------------
    search = st.text_input("🔍 Cerca cliente")

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["Nome"].str.contains(search, case=False) |
            filtered["PIVA"].str.contains(search, case=False)
        ]

    # -----------------------
    # CLIENT CARDS
    # -----------------------
    for _, c in filtered.iterrows():

        prezzo_finale = prezzo_base + c["Margine"] + c["Trasporto"]

        with st.container():

            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

            with col1:
                st.markdown(f"### 👤 {c['Nome']}")
                st.caption(f"P.IVA: {c['PIVA']}")

            with col2:
                st.metric("💰 €/L", f"{prezzo_finale:.3f}")

            with col3:
                msg = f"Carissimo {c['Nome']}, il prezzo di oggi è {prezzo_finale:.3f} €/L"
                wa_link = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"
                st.link_button("📲 WhatsApp", wa_link)

            with col4:

                if st.button("✏️ Edit", key=f"edit_{c['ID']}"):
                    st.session_state.edit_id = c["ID"]
                    st.sidebar.info("Vai su Nuovo Cliente per modificare")

                if st.button("🗑️ Delete", key=f"del_{c['ID']}"):
                    st.session_state.clienti = st.session_state.clienti[
                        st.session_state.clienti["ID"] != c["ID"]
                    ]
                    st.rerun()

        st.divider()

# -----------------------
# ADD / EDIT CLIENTE
# -----------------------
elif page == "➕ Nuovo Cliente":

    st.title("➕ Cliente")

    editing = st.session_state.edit_id is not None

    if editing:
        df_edit = st.session_state.clienti[
            st.session_state.clienti["ID"] == st.session_state.edit_id
        ]

        if df_edit.empty:
            st.warning("Cliente non trovato")
            st.stop()

        c = df_edit.iloc[0]
    else:
        c = {"Nome": "", "PIVA": "", "Telefono": "", "Margine": 0.0, "Trasporto": 0.0}

    nome = st.text_input("Nome", value=c["Nome"])
    piva = st.text_input("P.IVA", value=c["PIVA"])
    tel = st.text_input("Telefono", value=c["Telefono"])

    margine = st.number_input(
        "Margine",
        value=float(c["Margine"]),
        step=0.001,
        format="%.3f"
    )

    trasporto = st.number_input(
        "Trasporto",
        value=float(c["Trasporto"]),
        step=0.001,
        format="%.3f"
    )

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

            st.session_state.clienti = pd.concat(
                [st.session_state.clienti, new_row],
                ignore_index=True
            )

        st.success("Salvato con successo!")
        st.rerun()
