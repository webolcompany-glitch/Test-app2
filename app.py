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
# HEADER
# -----------------------
st.title("⛽ Fuel SaaS Platform")

df = st.session_state.clienti

# -----------------------
# TABS NAVIGATION (PRO UX)
# -----------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "👤 Clienti",
    "➕ Nuovo Cliente"
])

# =========================================================
# 📊 DASHBOARD
# =========================================================
with tab1:

    st.subheader("Dashboard")

    prezzo_base = st.number_input(
        "💰 Prezzo base oggi",
        value=float(st.session_state.prezzo_base),
        step=0.001,
        format="%.3f"
    )

    st.session_state.prezzo_base = prezzo_base

    clienti_count = len(df)
    media_margine = df["Margine"].mean()
    prezzo_medio = (prezzo_base + df["Margine"] + df["Trasporto"]).mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Base", f"{prezzo_base:.3f} €")
    col2.metric("👤 Clienti", clienti_count)
    col3.metric("📊 Margine", f"{media_margine:.3f}")
    col4.metric("⛽ Medio", f"{prezzo_medio:.3f}")

    st.divider()

    search = st.text_input("🔍 Cerca cliente")

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["Nome"].str.contains(search, case=False) |
            filtered["PIVA"].str.contains(search, case=False)
        ]

    for _, c in filtered.iterrows():

        prezzo_finale = prezzo_base + c["Margine"] + c["Trasporto"]

        with st.container():

            col1, col2, col3, col4 = st.columns([3,2,2,2])

            with col1:
                st.markdown(f"### 👤 {c['Nome']}")
                st.caption(c["PIVA"])

            with col2:
                st.metric("€/L", f"{prezzo_finale:.3f}")

            with col3:
                msg = f"Prezzo oggi {prezzo_finale:.3f} €/L"
                link = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"
                st.link_button("📲 WhatsApp", link)

            with col4:

                if st.button("✏️", key=f"edit_dash_{c['ID']}"):
                    st.session_state.edit_id = c["ID"]

                if st.button("🗑️", key=f"del_dash_{c['ID']}"):
                    st.session_state.clienti = df[df["ID"] != c["ID"]]
                    st.rerun()

        st.divider()

# =========================================================
# 👤 CLIENTI (VERSIONE MOBILE FRIENDLY MIGLIORATA)
# =========================================================
with tab2:

    st.subheader("Lista Clienti")

    for _, c in df.iterrows():

        col1, col2 = st.columns([4,1])

        with col1:
            st.markdown(f"""
            ### 👤 {c['Nome']}
            📄 P.IVA: {c['PIVA']}  
            📞 {c['Telefono']}  
            """)

            st.caption(f"Margine: {c['Margine']:.3f} | Trasporto: {c['Trasporto']:.3f}")

        with col2:

            st.write("")

            if st.button("✏️", key=f"edit_list_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                st.info("Vai su 'Nuovo Cliente' per modificare")

            if st.button("🗑️", key=f"del_list_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

        st.divider()

# =========================================================
# ➕ NUOVO CLIENTE (CREATE + EDIT)
# =========================================================
with tab3:

    st.subheader("Nuovo / Modifica Cliente")

    editing = st.session_state.edit_id is not None

    if editing:
        df_edit = df[df["ID"] == st.session_state.edit_id]

        if df_edit.empty:
            st.warning("Cliente non trovato")
            st.stop()

        c = df_edit.iloc[0]
    else:
        c = {"Nome": "", "PIVA": "", "Telefono": "", "Margine": 0.0, "Trasporto": 0.0}

    nome = st.text_input("Nome", value=c["Nome"])
    piva = st.text_input("P.IVA", value=c["PIVA"])
    tel = st.text_input("Telefono", value=c["Telefono"])

    margine = st.number_input("Margine", value=float(c["Margine"]), step=0.001, format="%.3f")
    trasporto = st.number_input("Trasporto", value=float(c["Trasporto"]), step=0.001, format="%.3f")

    if st.button("💾 Salva"):

        if editing:
            st.session_state.clienti.loc[
                st.session_state.clienti["ID"] == st.session_state.edit_id,
                ["Nome", "PIVA", "Telefono", "Margine", "Trasporto"]
            ] = [nome, piva, tel, margine, trasporto]

            st.session_state.edit_id = None

        else:
            new_id = int(df["ID"].max()) + 1

            new_row = pd.DataFrame([{
                "ID": new_id,
                "Nome": nome,
                "PIVA": piva,
                "Telefono": tel,
                "Margine": margine,
                "Trasporto": trasporto
            }])

            st.session_state.clienti = pd.concat([df, new_row], ignore_index=True)

        st.success("Salvato!")
        st.rerun()
