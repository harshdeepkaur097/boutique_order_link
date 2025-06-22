
# === app.py ===

import streamlit as st
import requests

st.set_page_config(page_title="Suit Tool", layout="wide")
st.title("💼 Punjabi Suit Tools")

backend_url = "https://boutique-order-link-backend.onrender.com"

# Sidebar Navigation
tool = st.sidebar.radio("Choose a Tool", [
    "Generate WhatsApp Link",
    "Decode Product Code",
])

if tool == "Generate WhatsApp Link":
    st.header("🧵 Generate Product Code & WhatsApp Message")
    with st.form("generate_form"):
        boutique_name = st.text_input("Boutique Name*")
        secret_key = st.text_input("Secret Key*", type="password")
        pinterest_link = st.text_input("Pinterest Product Link*")
        product_description = st.text_area("Product Description*")
        original_price = st.number_input("Original Price (INR)*", min_value=0.0, format="%.2f")
        commission = st.number_input("Commission to Add (INR)*", value=700.0, format="%.2f")

        submitted = st.form_submit_button("Generate")

    if submitted:
        res = requests.post(f"{backend_url}/encode", json={
            "boutique_name": boutique_name,
            "secret_key": secret_key,
            "pinterest_link": pinterest_link,
            "product_description": product_description,
            "original_price": original_price,
            "commission": commission
        })
        if res.ok:
            out = res.json()
            st.subheader("✅ Hidden Code")
            st.code(out['hidden_code'])
            st.subheader("📩 WhatsApp Message")
            st.text_area("Click to copy", out['whatsapp_message'], height=180)
            st.markdown(f"[🔗 Open WhatsApp Link]({out['whatsapp_link']})")
            st.subheader("📝 Product Description Block")
            st.text_area("Click to copy", out['product_description_output'], height=130)
        else:
            st.error(res.json().get("detail", "Something went wrong"))

elif tool == "Decode Product Code":
    st.header("🔍 Decode Boutique Name")
    with st.form("decode_form"):
        code_str = st.text_input("Enter Hidden Code (e.g. 12-5-8)")
        secret_key = st.text_input("Enter Secret Key", type="password")
        submitted = st.form_submit_button("Decode")

    if submitted:
        try:
            code = [int(i) for i in code_str.strip().split("-")]
            res = requests.post(f"{backend_url}/decode", json={
                "hidden_code": code,
                "secret_key": secret_key
            })
            if res.ok:
                out = res.json()
                st.success(f"Boutique Name: {out['boutique_name']}")
                st.write(f"Original Price: {out['original_price']}")
                st.write(f"Selling Price: {out['selling_price_inr']}")
                st.write(f"USD Price: {out['selling_price_usd']}")
            else:
                st.error(res.json().get("detail", "Error"))
        except:
            st.error("Invalid code format")
