import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel SaaS", layout="wide")

# -----------------------
# 🎨 GLOBAL CSS
# -----------------------
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #f9fafb;
}

/* NAVBAR */
.navbar {
    position: sticky;
    top: 0;
    background: white;
    padding: 10px 0;
    z-index: 999;
    border-bottom: 1px solid #eee;
}

/* CARD */
.card {
    padding: 18px;
    border-radius: 16px;
    background: #ffffff;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 12px;
}

/* KPI */
.kpi {
    text-align: center;
    padding: 18px;
    border-radius: 16px;
    background: linear-gradient(135deg, #111827, #1f2937);
    color: white;
}

/* BUTTON */
.stButton>button {
    border-radius: 10px;
    font-weight: 500;
    padding: 8px 12px;
}

/* MOBILE */
@media (max-width: 768px) {
    .card {
        padding: 14px;
    }
}

</style>
""", unsafe_allow_html=True)

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

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

df = st.session_state.clienti

# -----------------------
# NAVBAR
# -----------------------
st.markdown('<div class="navbar">', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("📊", use_container_width=True):
        st.session_state.page = "dashboard"

with c2:
    if st.button("👤", use_container_width=True):
        st.session_state.page = "clienti"

with c3:
    if st.button("➕", use_container_width=True):
        st.session_state.page = "cliente"

st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state.page

# =========================================================
# 📊 DASHBOARD
# =========================================================
if page == "dashboard":

    st.markdown("## ⛽ Dashboard")

    prezzo_base = st.number_input(
        "💰 Prezzo base",
        value=float(st.session_state.prezzo_base),
        step=0.001,
        format="%.3f"
    )

    st.session_state.prezzo_base = prezzo_base

    media_margine = df["Margine"].mean()
    clienti_count = len(df)
    prezzo_medio = (prezzo_base + df["Margine"] + df["Trasporto"]).mean()

    # KPI
    k1, k2, k3, k4 = st.columns(4)

    def kpi(label, value):
        st.markdown(f"""
        <div class="kpi">
            <div style="font-size:13px; opacity:0.7;">{label}</div>
            <div style="font-size:22px; font-weight:600;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    with k1:
        kpi("💰 Base", f"{prezzo_base:.3f} €")

    with k2:
        kpi("👤 Clienti", clienti_count)

    with k3:
        kpi("📊 Margine", f"{media_margine:.3f}")

    with k4:
        kpi("⛽ Prezzo", f"{prezzo_medio:.3f}")

    st.divider()

    # SEARCH
    search = st.text_input("🔍 Cerca cliente")

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["Nome"].str.contains(search, case=False) |
            filtered["PIVA"].str.contains(search, case=False)
        ]

    # CLIENT CARDS
    for _, c in filtered.iterrows():

        prezzo_finale = prezzo_base + c["Margine"] + c["Trasporto"]

        st.markdown(f"""
        <div class="card">
            <div style="font-size:18px; font-weight:600;">👤 {c['Nome']}</div>
            <div style="font-size:13px; color:gray;">P.IVA: {c['PIVA']}</div>

            <div style="margin-top:8px; font-size:20px; font-weight:600;">
                💰 {prezzo_finale:.3f} €/L
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2,1,1])

        with col1:
            msg = f"Prezzo oggi {prezzo_finale:.3f} €/L"
            link = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"

            st.markdown(f"""
            <a href="{link}" target="_blank" style="
                display:block;
                padding:10px;
                background:#22c55e;
                color:white;
                text-align:center;
                border-radius:10px;
                text-decoration:none;
                font-weight:500;
            ">
            📲 Invia WhatsApp
            </a>
            """, unsafe_allow_html=True)

        with col2:
            if st.button("✏️", key=f"edit_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                st.session_state.page = "cliente"

        with col3:
            if st.button("🗑️", key=f"del_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

# =========================================================
# 👤 CLIENTI
# =========================================================
elif page == "clienti":

    st.markdown("## 👤 Clienti")

    search = st.text_input("🔍 Cerca cliente")

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["Nome"].str.contains(search, case=False) |
            filtered["PIVA"].str.contains(search, case=False)
        ]

    for _, c in filtered.iterrows():

        st.markdown(f"""
        <div class="card">
            <div style="font-size:18px; font-weight:600;">👤 {c['Nome']}</div>
            <div style="font-size:13px; color:gray;">{c['PIVA']}</div>
            <div style="font-size:13px;">📞 {c['Telefono']}</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✏️ Modifica", key=f"edit_list_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                st.session_state.page = "cliente"

        with col2:
            if st.button("🗑️ Elimina", key=f"del_list_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

# =========================================================
# ➕ CLIENTE
# =========================================================
elif page == "cliente":

    st.markdown("## ➕ Cliente")

    editing = st.session_state.edit_id is not None

    if editing:
        c = df[df["ID"] == st.session_state.edit_id]

        if c.empty:
            st.warning("Cliente non trovato")
            st.stop()

        c = c.iloc[0]
    else:
        c = {"Nome": "", "PIVA": "", "Telefono": "", "Margine": 0.0, "Trasporto": 0.0}

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome", value=c["Nome"])
        piva = st.text_input("P.IVA", value=c["PIVA"])

    with col2:
        tel = st.text_input("Telefono", value=c["Telefono"])

    margine = st.number_input("Margine", value=float(c["Margine"]), step=0.001, format="%.3f")
    trasporto = st.number_input("Trasporto", value=float(c["Trasporto"]), step=0.001, format="%.3f")

    salva = st.button("💾 Salva", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if salva:

        if editing:
            st.session_state.clienti.loc[
                st.session_state.clienti["ID"] == st.session_state.edit_id,
                ["Nome", "PIVA", "Telefono", "Margine", "Trasporto"]
            ] = [nome, piva, tel, margine, trasporto]

            st.session_state.edit_id = None

        else:
            new_id = int(df["ID"].max()) + 1 if len(df) > 0 else 1

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
        st.session_state.page = "clienti"
        st.rerun()
