import streamlit as st
import requests

st.set_page_config(page_title="Suit Tool", layout="wide")
st.title("💼 Punjabi Suit Tools")

if "history" not in st.session_state:
    st.session_state.history = []

if "decoded_output" not in st.session_state:
    st.session_state.decoded_output = {}

backend_url = "https://boutique-order-link-backend.onrender.com"  # Use your deployed URL here

# Sidebar Navigation
tool = st.sidebar.radio("Choose a Tool", [
    "Create Product Code",
    "Find boutique name and real price",
    "📌 Pinterest ਲਈ Description ਬਣਾਓ"
])

def copy_button(text, key_suffix=None):
    key = f"copy_{key_suffix or text[:10]}"
    st.text_area("📋 Click below then Ctrl+C to copy", text, key=key, height=100)


# 1. Create Code
if tool == "Create Product Code":
    st.header("🎨 Create Product Code")
    with st.form("encode_form"):
        boutique_name = st.text_input("Boutique Name")
        price = st.text_input("Price")
        video_link = st.text_input("Video Link (optional)")
        secret_key = st.text_input("Secret Key", type="password")
        submitted = st.form_submit_button("Generate")

    if submitted:
        res = requests.post(f"{backend_url}/encode", json={
            "boutique_name": boutique_name,
            "price": price,
            "video_link": video_link,
            "secret_key": secret_key
        })
        if res.ok:
            out = res.json()
            st.session_state.history.append(out)
            st.subheader("✅ Hidden Code")
            st.code(out['hidden_code'])
            copy_button(out['hidden_code'], "copy_hidden")
            st.markdown(f"[💬 Order on WhatsApp]({out['whatsapp_link']})")
            copy_button(out['whatsapp_link'], "copy_wa")
        else:
            st.error(res.json().get("error", "Unknown error"))

# 2. Decode Code
elif tool == "Find boutique name and real price":
    st.header("🔍 Find boutique name and real price")
    with st.form("decode_form"):
        hidden_code = st.text_input("Enter Hidden Code")
        secret_key = st.text_input("Enter Your Secret Key", type="password")
        submitted = st.form_submit_button("Decode")

    if submitted:
        res = requests.post(f"{backend_url}/decode", json={
            "hidden_code": hidden_code,
            "secret_key": secret_key
        })
        if res.ok:
            out = res.json()
            st.session_state.history.append(out)
            st.session_state.decoded_output = out

            st.subheader("🏷️ Boutique Name")
            st.success(out['boutique_name'])
            copy_button(out['boutique_name'], "copy_name")

            st.write(f"💰 Original Price: ₹{out['original_price']}")
            st.write(f"💵 Selling Price: ₹{out['selling_price_inr']} / ${out['selling_price_usd']}")
            st.markdown(f"[💬 Order on WhatsApp]({out['whatsapp_link']})")
            copy_button(out['whatsapp_link'], "copy_decoded_wa")
        else:
            st.error(res.json().get("error", "Unauthorized or invalid code"))

# 3. Description Tool
elif tool == "📌 Pinterest ਲਈ Description ਬਣਾਓ":
    st.header("📌 Pinterest ਲਈ Description ਬਣਾਓ")
    default_name = st.session_state.decoded_output.get("boutique_name", "")
    default_price = st.session_state.decoded_output.get("selling_price_inr", "")

    boutique_name = st.text_input("ਬੁਟੀਕ ਦਾ ਨਾਂ", value=default_name)
    price = st.text_input("ਕੀਮਤ", value=str(default_price))

    if st.button("✨ Description ਬਣਾਓ"):
        if boutique_name and price:
            desc = f"""✨ {boutique_name} | Premium Punjabi Suit ✨
🧵 Custom-made suit starting at ₹{price}!
💃 Stylish | Comfortable | Made with love.
📦 Free Shipping in India / Extra for International.
📲 Order now on WhatsApp!"""

            st.text_area("Generated Description", desc, height=130)
            copy_button(desc, "copy_description")
        else:
            st.warning("ਕਿਰਪਾ ਕਰਕੇ Boutique Name ਅਤੇ Price ਭਰੋ।")

# History Section
if st.session_state.history:
    st.markdown("---")
    st.subheader("🕘 Previous Results")
    for item in st.session_state.history[::-1]:
        st.json(item)
