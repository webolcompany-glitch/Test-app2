import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel SaaS", layout="wide")

# -----------------------
# DATA
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
# DETECT MOBILE (APPROX)
# -----------------------
is_mobile = st.sidebar.checkbox("📱 Modalità Mobile (test)", value=True)

# -----------------------
# MENU SIMPLE
# -----------------------
page = st.radio("MENU", ["📊 Dashboard", "👤 Clienti", "➕ Cliente"], horizontal=not is_mobile)

# =========================================================
# 📊 DASHBOARD MOBILE FIRST
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

    # KPI (2 per riga su mobile)
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

    # -----------------------
    # MOBILE CARDS (IMPORTANT)
    # -----------------------
    for _, c in filtered.iterrows():

        prezzo_finale = prezzo_base + c["Margine"] + c["Trasporto"]

        st.markdown(f"""
        ## 👤 {c['Nome']}
        📄 P.IVA: {c['PIVA']}  
        💰 Prezzo: **{prezzo_finale:.3f} €/L**
        """)

        col1, col2 = st.columns(2)

        with col1:
            msg = f"Prezzo oggi {prezzo_finale:.3f} €/L"
            link = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"
            st.link_button("📲 WhatsApp", link, use_container_width=True)

        with col2:
            if st.button("🗑️ Elimina", key=f"del_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

        st.divider()

# =========================================================
# 👤 CLIENTI MOBILE LIST
# =========================================================
elif page == "👤 Clienti":

    st.title("Clienti")

    for _, c in df.iterrows():

        st.markdown(f"""
        ### 👤 {c['Nome']}
        📞 {c['Telefono']}  
        📄 {c['PIVA']}
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✏️ Edit", key=f"edit_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                st.info("Vai su tab Cliente")

        with col2:
            if st.button("🗑️ Delete", key=f"del2_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

        st.divider()

# =========================================================
# ➕ CREATE / EDIT
# =========================================================
elif page == "➕ Cliente":

    st.title("Nuovo Cliente")

    editing = st.session_state.edit_id is not None

    if editing:
        c = df[df["ID"] == st.session_state.edit_id].iloc[0]
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

        else:
            new_id = int(df["ID"].max()) + 1

            st.session_state.clienti.loc[len(df)] = [
                new_id, nome, piva, tel, margine, trasporto
            ]

        st.success("Salvato!")
        st.rerun()
