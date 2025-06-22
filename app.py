import streamlit as st
import requests

API_BASE = "https://boutique-order-link-backend.onrender.com"

st.set_page_config(page_title="Punjabi Suit Code Tool", layout="centered")
st.title("👗 Punjabi Suit Code Generator")

lang = st.radio("🌐 Language / ਭਾਸ਼ਾ ਚੁਣੋ", ["English", "ਪੰਜਾਬੀ"])

if lang == "English":
    st.info("""
🔐 **Why Use a Secret Key?**

- 🛡️ **Protect your boutique name & real price** — no one can decode your product codes without your key  
- ♾️ **Unlimited usage** — no daily limits or restrictions

💰 **Only ₹2000/month** – starting price

👉 [Get your Secret Key on WhatsApp](https://wa.me/+917973567740)
""")
else:
    st.info("""
🔐 **ਸਿਕਰਟ ਕੀ ਕਿਉਂ ਲਓ?**

- 🛡️ **ਬੁਟੀਕ ਦਾ ਨਾਂ ਅਤੇ ਅਸਲੀ ਰੇਟ ਲੁਕਾਓ** — ਤੁਹਾਡੇ ਕੋਡ ਕੋਈ ਹੋਰ ਡੀਕੋਡ ਨਹੀਂ ਕਰ ਸਕਦਾ  
- ♾️ **ਅਣਗਿਣਤ ਵਰਤੋਂ** — ਰੋਜ਼ਾਨਾ ਵਰਤੋਂ ਦੀ ਕੋਈ ਸੀਮਾ ਨਹੀਂ

💰 **ਸਿਰਫ ₹2000/ਮਹੀਨਾ** – ਸ਼ੁਰੂਆਤੀ ਕੀਮਤ

👉 [WhatsApp ਤੇ ਆਪਣੀ Secret Key ਲਵੋ](https://wa.me/+917973567740)
""")


if "generated" not in st.session_state:
    st.session_state.generated = False

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

MAX_DAILY_USAGE = 5
MASTER_SECRET = "cr123"  # Replace with your actual master key

custom_messages = {
    "delivery_time": "🧵 All suits are custom-made & take 5–20 days to prepare.",
    "shipping_extra": "(Shipping extra – we’ll confirm after order.)",
    "shipping_free": "(Free shipping within India)"
}

st.sidebar.header("⚙️ Settings")
with st.sidebar.expander("Customize Text Messages"):
    for key in custom_messages:
        custom_messages[key] = st.text_input(f"{key.replace('_', ' ').title()}", custom_messages[key])

st.markdown("---")

secret_key = st.text_input("🔐 Your Secret Key", type="password")

if secret_key:
    with st.form("generate_form"):
        boutique_name = st.text_input("Boutique Name")
        price = st.text_input("Base Price (INR)")
        video_link = st.text_input("Video Link (Optional)")
        submit_button = st.form_submit_button("Generate Code")

    if submit_button:
        if st.session_state.usage_count >= MAX_DAILY_USAGE and secret_key != MASTER_SECRET:
            st.warning("⚠️ Daily usage limit reached. Please try again tomorrow or support us on BuyMeACoffee.")
        else:
            payload = {
                "boutique_name": boutique_name,
                "price": price,
                "video_link": video_link,
                "secret_key": secret_key,
                "custom_messages": custom_messages
            }
            try:
                res = requests.post(f"{API_BASE}/encode", json=payload)
                data = res.json()
                if res.status_code == 200:
                    st.success("✅ Code Generated Successfully!")
                    st.code(data['hidden_code'], language="text")
                    st.markdown(f"[Click to open WhatsApp link 🔗]({data['whatsapp_link']})")

                    st.session_state.generated = True
                    st.session_state.usage_count += 1

                    with st.expander("📌 Pinterest ਲਈ Description ਬਣਾਓ"):
                        user_description = st.text_area("ਰੇਟ ਮਿਟਾ ਕੇ description ਲਿਖੋ")
                        if user_description:
                            st.markdown("**📋 Final Output**")
                            output_text = f"₹{data['selling_price_inr']}\n{data['hidden_code']}\n{user_description}"
                            st.code(output_text, language="text")
                            if st.button("📋 Copy All"):
                                st.text_area("📋 Copy Manually", output_text)
                else:
                    st.error(data.get("error", "Something went wrong"))
            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.markdown("---")
    with st.form("decode_form"):
        st.subheader("🔎 Decode a Product Code")
        hidden_code = st.text_input("Enter Hidden Code")
        decode_button = st.form_submit_button("Decode")

    if decode_button:
        try:
            res = requests.post(f"{API_BASE}/decode", json={"hidden_code": hidden_code, "secret_key": secret_key})
            data = res.json()
            if res.status_code == 200:
                st.success("✅ Decoded Successfully")
                st.json(data)
            else:
                st.error(data.get("error", "Unauthorized or invalid code."))
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.info("🔐 Please enter your secret key to continue.")
