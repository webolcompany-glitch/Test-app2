import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel SaaS", layout="wide")

# -----------------------
# DATA INIT
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

df = st.session_state.clienti

# -----------------------
# MOBILE NAV (UNIFICATO)
# -----------------------
page = st.radio(
    "MENU",
    ["📊 Dashboard", "👤 Clienti", "➕ Cliente"],
    horizontal=True
)

# =========================================================
# 📊 DASHBOARD MOBILE-FIRST (GIÀ OK + MIGLIORATO COERENTE)
# =========================================================
if page == "📊 Dashboard":

    st.title("⛽ Dashboard")

    prezzo_base = st.number_input(
        "💰 Prezzo base",
        value=float(st.session_state.prezzo_base),
        step=0.001,
        format="%.3f"
    )

    st.session_state.prezzo_base = prezzo_base

    # KPI (mobile style)
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    col1.metric("💰 Base", f"{prezzo_base:.3f}")
    col2.metric("👤 Clienti", len(df))
    col3.metric("📊 Margine", f"{df['Margine'].mean():.3f}")
    col4.metric("⛽ Medio", f"{(prezzo_base + df['Margine'] + df['Trasporto']).mean():.3f}")

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

        st.markdown(f"""
        ### 👤 {c['Nome']}
        📄 P.IVA: {c['PIVA']}  
        💰 **{prezzo_finale:.3f} €/L**
        """)

        col1, col2 = st.columns(2)

        with col1:
            msg = f"Prezzo oggi {prezzo_finale:.3f} €/L"
            link = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"
            st.link_button("📲 WhatsApp", link, use_container_width=True)

        with col2:
            if st.button("🗑️ Elimina", key=f"del_dash_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

        st.divider()

# =========================================================
# 👤 CLIENTI (MOBILE CARDS UNIFORMI)
# =========================================================
elif page == "👤 Clienti":

    st.title("Clienti")

    search = st.text_input("🔍 Cerca cliente")

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["Nome"].str.contains(search, case=False) |
            filtered["PIVA"].str.contains(search, case=False)
        ]

    for _, c in filtered.iterrows():

        st.markdown(f"""
        ## 👤 {c['Nome']}
        📄 P.IVA: {c['PIVA']}  
        📞 {c['Telefono']}  
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✏️ Modifica", key=f"edit_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                st.info("Vai su ➕ Cliente per modificare")

        with col2:
            if st.button("🗑️ Elimina", key=f"del_list_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

        st.divider()

# =========================================================
# ➕ CREATE / EDIT CLIENTE (COERENTE MOBILE)
# =========================================================
elif page == "➕ Cliente":

    st.title("Cliente")

    editing = st.session_state.edit_id is not None

    if editing:
        c = df[df["ID"] == st.session_state.edit_id]

        if c.empty:
            st.warning("Cliente non trovato")
            st.stop()

        c = c.iloc[0]
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
