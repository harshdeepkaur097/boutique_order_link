import streamlit as st
import requests

BACKEND_URL = "http://localhost:5001"  # Change if deployed

st.title("🧵 WhatsApp ਆਰਡਰ ਟੂਲ")

st.header("ਪੈਸੇ ਹੀ ਪੈਸੇ")
with st.form("encode_form_2"):
    col1, col2 = st.columns(2)
    with col1:
        boutique = st.text_input("ਬੁਟੀਕ ਦਾ ਨਾਂ", placeholder="e.g., mehar_boutique01")
    with col2:
        price = st.text_input("ਅਸਲੀ ਰੇਟ", placeholder="e.g., 3800")
    video_link = st.text_input("ਵੀਡੀਓ ਜਾਂ ਫੋਟੋ pinterest 'ਤੇ ਪਾ ਆਓ, ਉਸਤੋਂ ਬਾਅਦ ਉਸਦਾ ਲਿੰਕ ਇਥੇ paste ਕਰੋ")
    encode_submit = st.form_submit_button("ਲਿੰਕ ਬਣਾਓ")

    if encode_submit:
        payload = {
            "boutique_name": boutique,
            "price": price,
            "video_link": video_link
        }
        response = requests.post(f"{BACKEND_URL}/encode", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success(f"🆔 ਕੋਡ ਬਣ ਗਿਆ: {data['hidden_code']}")
            st.code(data['whatsapp_link'], language="")
        else:
            st.error(f"Error: {response.json().get('error', 'Failed to encode')}")

st.header("ਕੋਡ ਤੋਂ ਪਤਾ ਲਗਾਓ ਬੁਟੀਕ ਦਾ ਨਾਂ ਤੇ ਰੇਟ")
with st.form("decode_form_1"):
    hidden_code = st.text_input("ਲੰਮੇ ਅੱਖਰਾਂ ਵਾਲਾ ਕੋਡ ਭਰੋ")
    decode_submit = st.form_submit_button("ਦੱਸੋ ਕਿਸਦਾ ਸੂਟ ਆ ਇਹ ਤੇ ਕਿੰਨੇ ਦਾ ਹੈ")

    if decode_submit:
        payload = {"hidden_code": hidden_code}
        response = requests.post(f"{BACKEND_URL}/decode", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success(f"ਬੁਟੀਕ: {data['decoded_name']}")
            st.info(f"ਅਸਲੀ ਰੇਟ: ₹{data['original_price']}")
            st.info(f"ਵੇਚਣ ਵਾਲਾ ਰੇਟ: ₹{data['selling_price_inr']} / ${data['selling_price_usd']}")
            st.code(data['whatsapp_link'], language="")
        else:
            st.error(f"Error: {response.json().get('error', 'Failed to decode')}")
