import streamlit as st
import requests

BACKEND_URL = "https://boutique-order-link-backend.onrender.com"  # Change if deployed

st.title("🧵 WhatsApp ਆਰਡਰ ਟੂਲ")

with st.form("encode_form_2"):
    col1, col2 = st.columns(2)
    with col1:
        boutique = st.text_input("ਬੁਟੀਕ ਦਾ ਸਿਰਫ਼ ਕੋਡ ਭਰੋ - ਪੂਰਾ ਨਾਂ ਨਹੀਂ ਲਿਖਣਾ", placeholder="e.g., CR")
    with col2:
        price = st.text_input("ਅਸਲੀ ਰੇਟ", placeholder="e.g., 3800")
    
    video_link = st.text_input("ਵੀਡੀਓ ਜਾਂ ਫੋਟੋ pinterest 'ਤੇ ਪਾ ਆਓ, ਉਸਤੋਂ ਬਾਅਦ ਉਸਦਾ ਲਿੰਕ ਇਥੇ paste ਕਰੋ")

    with st.expander("📱 Add custom details (optional)"):
        phone_number = st.text_input("📞 WhatsApp Number", value="917973567740")
        razorpay_link = st.text_input("💸 Razorpay Link", value="https://razorpay.me/@merapunjabisuit")
        paypal_link = st.text_input("🌍 PayPal Link", value="https://paypal.me/parmjitkaur0069")

    encode_submit = st.form_submit_button("ਲਿੰਕ ਬਣਾਓ")

    if encode_submit:
        payload = {
            "boutique_name": boutique,
            "price": price,
            "video_link": video_link,
            "phone_number": phone_number,
            "razorpay_link": razorpay_link,
            "paypal_link": paypal_link
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
