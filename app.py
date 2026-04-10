import streamlit as st
import pandas as pd

st.title("⛽ Fuel Manager Dashboard")

# -----------------------
# PREZZO BASE
# -----------------------
prezzo_base = st.number_input("💰 Prezzo base oggi (€)", value=1.00, step=0.01)

st.divider()

st.subheader("👤 Clienti")

# -----------------------
# DATI MOCK (poi DB vero)
# -----------------------
if "clienti" not in st.session_state:
    st.session_state.clienti = pd.DataFrame([
        {"Nome": "Mario SRL", "PIVA": "123", "Telefono": "333111", "Margine": 0.05, "Trasporto": 0.02},
        {"Nome": "Luca Trasporti", "PIVA": "456", "Telefono": "333222", "Margine": 0.04, "Trasporto": 0.03},
    ])

df = st.session_state.clienti

# -----------------------
# CARDS CLIENTI
# -----------------------
for i, row in df.iterrows():

    prezzo_finale = prezzo_base + row["Margine"] + row["Trasporto"]

    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        st.markdown(f"### 👤 {row['Nome']}")
        st.caption(f"P.IVA: {row['PIVA']}")

    with col2:
        st.metric("💰 Prezzo", f"{prezzo_finale:.3f} €/L")

    with col3:
        msg = f"Carissimo {row['Nome']}, il prezzo di oggi è {prezzo_finale:.3f} €/L"
        wa_link = f"https://wa.me/{row['Telefono']}?text={msg.replace(' ', '%20')}"

        st.link_button("📲 Invia WhatsApp", wa_link)

    st.divider()
