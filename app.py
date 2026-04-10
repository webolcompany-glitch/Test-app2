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
# NAVIGATION (APP STYLE)
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"

with c2:
    if st.button("👤 Clienti", use_container_width=True):
        st.session_state.page = "clienti"

with c3:
    if st.button("➕ Cliente", use_container_width=True):
        st.session_state.page = "cliente"

page = st.session_state.page

st.divider()

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

    # -----------------------
    # KPI (FIXED + SPACING + LABELS)
    # -----------------------
    media_margine = df["Margine"].mean()
    clienti_count = len(df)
    prezzo_medio = (prezzo_base + df["Margine"] + df["Trasporto"]).mean()

    st.markdown("### 📊 Riepilogo")

    k1, k2 = st.columns(2, gap="large")
    k3, k4 = st.columns(2, gap="large")

    with k1:
        st.markdown(f"""
        <div style="
            padding:14px;
            border-radius:14px;
            background:#111827;
            color:white;
            text-align:center;
            margin-bottom:10px;
        ">
        <div style="font-size:12px;opacity:0.7;">💰 Base</div>
        <div style="font-size:20px;font-weight:600">{prezzo_base:.3f} €</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div style="
            padding:14px;
            border-radius:14px;
            background:#111827;
            color:white;
            text-align:center;
            margin-bottom:10px;
        ">
        <div style="font-size:12px;opacity:0.7;">👤 Clienti</div>
        <div style="font-size:20px;font-weight:600">{clienti_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div style="
            padding:14px;
            border-radius:14px;
            background:#111827;
            color:white;
            text-align:center;
            margin-top:10px;
        ">
        <div style="font-size:12px;opacity:0.7;">📊 Margine medio</div>
        <div style="font-size:20px;font-weight:600">{media_margine:.3f}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div style="
            padding:14px;
            border-radius:14px;
            background:#111827;
            color:white;
            text-align:center;
            margin-top:10px;
        ">
        <div style="font-size:12px;opacity:0.7;">⛽ Prezzo medio</div>
        <div style="font-size:20px;font-weight:600">{prezzo_medio:.3f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # -----------------------
    # CLIENTI (NON MODIFICATO COME RICHIESTO)
    # -----------------------
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

        col1, col2, col3 = st.columns(3)

        with col1:
            msg = f"Prezzo oggi {prezzo_finale:.3f} €/L"
            link = f"https://wa.me/{c['Telefono']}?text={msg.replace(' ', '%20')}"

            st.markdown(
                f"""
                <a href="{link}" target="_blank" style="
                    display:inline-block;
                    padding:6px 10px;
                    font-size:12px;
                    background:#22c55e;
                    color:white;
                    border-radius:8px;
                    text-decoration:none;
                    text-align:center;
                    width:100%;
                ">
                📲 WhatsApp
                </a>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if st.button("✏️", key=f"edit_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                st.session_state.page = "cliente"

        with col3:
            if st.button("🗑️", key=f"del_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

        st.divider()

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
        ### 👤 {c['Nome']}
        📄 {c['PIVA']}  
        📞 {c['Telefono']}
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✏️ Modifica", key=f"edit_list_{c['ID']}"):
                st.session_state.edit_id = c["ID"]
                st.session_state.page = "cliente"

        with col2:
            if st.button("🗑️ Elimina", key=f"del_list_{c['ID']}"):
                st.session_state.clienti = df[df["ID"] != c["ID"]]
                st.rerun()

        st.divider()

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
        st.session_state.page = "clienti"
        st.rerun()
