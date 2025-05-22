import streamlit as st
import requests
import urllib.parse

# --- CONFIGURAZIONE SECRETS ---
SHOPIFY_TOKEN = st.secrets["SHOPIFY_TOKEN"]
SHOPIFY_SHOP = st.secrets["SHOPIFY_SHOP"]
API_VERSION = "2024-01"

# --- FUNZIONE PER OTTENERE DETTAGLI ORDINE ---
def get_order_details(order_number):
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN
    }
    encoded_order_number = urllib.parse.quote(order_number)
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/orders.json?name={encoded_order_number}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        orders = response.json().get("orders", [])
        return orders[0] if orders else None
    else:
        st.error(f"Errore nella richiesta a Shopify: {response.status_code}")
        return None

# --- UI STREAMLIT ---
st.title("📦 Invio Anteprima Ordine - WOWSTAMPA")

order_input = st.text_input("🔎 Inserisci numero ordine (es. #WW12345)")

if st.button("Cerca ordine"):
    with st.spinner("🔍 Cerco l'ordine su Shopify..."):
        ordine = get_order_details(order_input)

    if ordine:
        phone = ordine.get("shipping_address", {}).get("phone", "").replace(" ", "").replace("-", "")
        if phone:
            st.success(f"📱 Numero trovato: {phone}")

            ordine_pulito = order_input.replace("#WW", "").strip()

            msg = f"""{ordine_pulito}

*ANTEPRIMA DI STAMPA*

Gentile cliente,

Le alleghiamo un’anteprima di stampa del suo ordine, *rilegga con attenzione e confermi per procedere con la stampa.*

*Dopo la conferma il file viene ritenuto idoneo per la stampa, eventuali modifiche non potranno essere effettuate.*

Le basterà confermare in risposta a questo messaggio!

Le ricordo che ha a disposizione 3 modifiche gratuite (ex: variazione colori, aggiunta di una frase), dopo di che saranno a pagamento.

Cordiali saluti,
WowStampa"""

            whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(msg)}"
            st.markdown(f"[📤 Clicca qui per aprire WhatsApp Web con il messaggio]({whatsapp_url})", unsafe_allow_html=True)
        else:
            st.warning("⚠️ L'ordine non contiene un numero di telefono.")
    else:
        st.error("❌ Ordine non trovato.")

