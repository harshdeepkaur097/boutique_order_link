import streamlit as st
import requests

st.set_page_config(page_title="Suit Tool", layout="wide")
st.title("💼 Punjabi Suit Code Tool")

backend_url = "https://boutique-order-link-backend.onrender.com"  # Replace if hosted elsewhere

# Sidebar
page = st.sidebar.radio("Select Tool", [
    "🛍️ Create Product Code",
    "🔎 Decode Product Code",
    "📌 Generate Pinterest Description"
])

def copy_button(text, label):
    st.text_area(f"📋 {label} (Click + Ctrl+C)", text, height=100)

# Encode Tool
if page == "🛍️ Create Product Code":
    st.header("🛠️ Generate Hidden Product Code")

    with st.form("encode_form"):
        boutique = st.text_input("Boutique Name")
        price = st.text_input("Original Price (₹)")
        desc = st.text_area("Product Description")
        video = st.text_input("Pinterest/Video Link")
        key = st.text_input("Secret Key", type="password")

        with st.expander("✏️ Customize Messages"):
            delivery = st.text_input("Delivery Note", "🧵 Custom-made, 5–20 days.")
            ship_in = st.text_input("Shipping Note (India)", "(Free shipping in India)")
            ship_int = st.text_input("Shipping Note (International)", "(Extra shipping charges apply)")

        submit = st.form_submit_button("Generate")

    if submit:
        payload = {
            "boutique_name": boutique,
            "price": price,
            "video_link": video,
            "secret_key": key,
            "description": desc,
            "custom_messages": {
                "delivery_time": delivery,
                "shipping_free": ship_in,
                "shipping_extra": ship_int
            }
        }
        r = requests.post(f"{backend_url}/encode", json=payload)
        if r.ok:
            data = r.json()

            st.success("✅ Code Generated!")
            st.code(data["hidden_code"])
            copy_button(data["hidden_code"], "Hidden Code")

            st.write(f"💰 **Selling Price**: ₹{data['selling_price_inr']} / ${data['selling_price_usd']}")
            st.markdown(f"[💬 Order on WhatsApp]({data['whatsapp_link']})")
            copy_button(data["whatsapp_link"], "WhatsApp Link")

            st.subheader("📝 Description Block")
            copy_button(data["product_description"], "Product Description")

        else:
            st.error(r.json().get("error", "Something went wrong."))

# Decode Tool
elif page == "🔎 Decode Product Code":
    st.header("🔍 Decode Hidden Code")
    with st.form("decode_form"):
        code = st.text_input("Enter Hidden Code")
        key = st.text_input("Secret Key", type="password")
        go = st.form_submit_button("Decode")

    if go:
        r = requests.post(f"{backend_url}/decode", json={"hidden_code": code, "secret_key": key})
        if r.ok:
            data = r.json()
            st.success(f"🏷️ Boutique: {data['boutique_name']}")
            st.write(f"🧾 Original Price: ₹{data['original_price']}")
            st.write(f"💵 Selling Price: ₹{data['selling_price_inr']} / ${data['selling_price_usd']}")
            st.markdown(f"[💬 WhatsApp Link]({data['whatsapp_link']})")
            copy_button(data["whatsapp_link"], "WhatsApp Link")
        else:
            st.error(r.json().get("error", "Invalid code or key"))

# Pinterest Description Tool
elif page == "📌 Generate Pinterest Description":
    st.header("📌 Generate Description for Pinterest")
    name = st.text_input("Boutique Name")
    price = st.text_input("Selling Price (₹)")

    if st.button("Generate Description"):
        if name and price:
            msg = f"""✨ {name} | Premium Punjabi Suit ✨
🧵 Custom-made suit starting at ₹{price}!
💃 Stylish | Comfortable | Made with love.
📦 Free Shipping in India / Extra for International.
📲 Order now on WhatsApp!"""
            copy_button(msg, "Pinterest Description")
        else:
            st.warning("Please fill both Boutique Name and Price.")
