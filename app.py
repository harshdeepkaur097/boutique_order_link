import streamlit as st
import requests

st.set_page_config(page_title="Punjabi Suit Tools", layout="wide")
st.title("💼 Boutique Order Link Generator")

if "history" not in st.session_state:
    st.session_state.history = []

if "decoded_output" not in st.session_state:
    st.session_state.decoded_output = {}

backend_url = "https://boutique-order-link-backend.onrender.com"

# Sidebar Navigation
tool = st.sidebar.radio("🔧 Choose a Tool", [
    "1️⃣ Create Product Code",
    "2️⃣ Decode Product Code",
    "3️⃣ Generate WhatsApp Order Link",
    "4️⃣ 📌 Pinterest Description"
])

def copy_button(text, key_suffix):
    key = f"copy_{key_suffix}"
    st.text_area("📋 Click below then Ctrl+C to copy", text, key=key, height=100)

# Tool 1: Create Product Code
if tool == "1️⃣ Create Product Code":
    st.header("🎨 Create Product Code")
    with st.form("encode_form"):
        boutique_name = st.text_input("🏷️ Boutique Name")
        secret_key = st.text_input("🔑 Secret Key", type="password")
        submitted = st.form_submit_button("✨ Generate Code")

    if submitted:
        res = requests.post(f"{backend_url}/encode", json={
            "boutique_name": boutique_name,
            "secret_key": secret_key
        })
        if res.ok:
            out = res.json()
            st.session_state.history.append(out)
            st.subheader("✅ Hidden Code")
            st.code(out['hidden_code'])
            copy_button(out['hidden_code'], "generated_code")
        else:
            st.error(res.json().get("error", "❌ Unknown error occurred."))

# Tool 2: Decode Product Code
elif tool == "2️⃣ Decode Product Code":
    st.header("🔍 Decode Product Code")
    with st.form("decode_form"):
        hidden_code = st.text_input("🔢 Hidden Code")
        secret_key = st.text_input("🔑 Secret Key", type="password")
        submitted = st.form_submit_button("🔓 Decode")

    if submitted:
        res = requests.post(f"{backend_url}/decode", json={
            "hidden_code": hidden_code,
            "secret_key": secret_key
        })
        if res.ok:
            out = res.json()
            st.session_state.history.append(out)
            st.session_state.decoded_output = out

            st.success(f"🏷️ Boutique Name: {out['boutique_name']}")
            st.write(f"💰 Original Price: ₹{out['original_price']}")
            st.write(f"💵 Selling Price: ₹{out['selling_price_inr']} / ${out['selling_price_usd']}")
            st.markdown(f"[💬 WhatsApp Order Link]({out['whatsapp_link']})")
            copy_button(out['whatsapp_link'], "decoded_whatsapp")
        else:
            st.error(res.json().get("error", "❌ Invalid code or key."))

# Tool 3: WhatsApp Link Generator
elif tool == "3️⃣ Generate WhatsApp Order Link":
    st.header("💬 WhatsApp Order Link Generator")
    with st.form("wa_form"):
        pin_url = st.text_input("📌 Pinterest URL")
        product_data = st.text_area("🧵 Product Description")
        original_price = st.text_input("💰 Original Price")
        boutique_name = st.text_input("🏷️ Boutique Name")
        secret_key = st.text_input("🔑 Secret Key", type="password")
        submitted = st.form_submit_button("🚀 Generate WhatsApp Message")

    with st.expander("⚙️ Optional Configs"):
        phone = st.text_input("📞 Phone", value="917973567740")
        razor = st.text_input("🇮🇳 Razorpay", value="https://razorpay.me/@merapunjabisuit")
        paypal = st.text_input("🌍 PayPal", value="https://paypal.me/parmjitkaur0069")

    if submitted:
        res = requests.post(f"{backend_url}/generate_message", json={
            "pin_url": pin_url,
            "product_data": product_data,
            "original_price": original_price,
            "boutique_name": boutique_name,
            "secret_key": secret_key,
            "phone_number": phone,
            "razorpay_link": razor,
            "paypal_link": paypal
        })
        if res.ok:
            out = res.json()
            st.success("✅ WhatsApp Message Generated")
            st.text_area("📦 WhatsApp Order Message", out['whatsapp_message'], height=200)
            copy_button(out['whatsapp_message'], "wa_msg")
        else:
            st.error(res.json().get("error", "❌ Could not generate link."))

# Tool 4: Pinterest Description
elif tool == "4️⃣ 📌 Pinterest Description":
    st.header("📌 Pinterest Description Generator")
    default_name = st.session_state.decoded_output.get("boutique_name", "")
    default_price = st.session_state.decoded_output.get("selling_price_inr", "")

    boutique_name = st.text_input("🏷️ Boutique Name", value=default_name)
    price = st.text_input("💰 Price", value=str(default_price))

    if st.button("✨ Generate Description"):
        if boutique_name and price:
            desc = f"""✨ {boutique_name} | Premium Punjabi Suit ✨\n🧵 Custom-made suit starting at ₹{price}!\n💃 Stylish | Comfortable | Made with love.\n📦 Free Shipping in India / Extra for International.\n📲 Order now on WhatsApp!"""
            st.text_area("📝 Generated Description", desc, height=150)
            copy_button(desc, "pinterest_desc")
        else:
            st.warning("⚠️ Please fill both Boutique Name and Price.")

# History
if st.session_state.history:
    st.markdown("---")
    st.subheader("🕘 History")
    for item in st.session_state.history[::-1]:
        st.json(item)
