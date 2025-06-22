import streamlit as st
import requests
import pyperclip

API_BASE = "https://boutique-order-link-backend.onrender.com"

st.set_page_config(page_title="Punjabi Suit Code Tool", layout="centered")
st.title("👗 Punjabi Suit Code Generator")

if "generated" not in st.session_state:
    st.session_state.generated = False

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

MAX_DAILY_USAGE = 5

def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success("Copied to clipboard!")

st.markdown("---")

secret_key = st.text_input("🔐 Your Secret Key", type="password")

# 🛠️ Advanced Boutique Settings (Collapsible)
if secret_key:
    with st.expander("⚙️ Boutique Defaults"):
        col1, col2 = st.columns(2)
        with col1:
            custom_line_1 = st.text_area("🧵 Delivery Time Line", value=st.session_state.get("custom_line_1", "🧵 All suits are custom-made & take 5–20 days to prepare."))
            custom_line_3 = st.text_area("📦 India Shipping Line", value=st.session_state.get("custom_line_3", "(Free shipping within India)"))
        with col2:
            custom_line_2 = st.text_area("🌍 Intl Shipping Line", value=st.session_state.get("custom_line_2", "(Shipping extra – we’ll confirm after order.)"))

        # Save settings in session
        st.session_state["custom_line_1"] = custom_line_1
        st.session_state["custom_line_2"] = custom_line_2
        st.session_state["custom_line_3"] = custom_line_3

    with st.form("generate_form"):
        boutique_name = st.text_input("Boutique Name")
        price = st.text_input("Base Price (INR)")
        video_link = st.text_input("Video Link (Optional)")
        submit_button = st.form_submit_button("Generate Code")

    if submit_button:
        if st.session_state.usage_count >= MAX_DAILY_USAGE and secret_key != "your_master_key_here":
            st.warning("⚠️ Daily usage limit reached. Please try again tomorrow or support us on BuyMeACoffee.")
        else:
            payload = {
                "boutique_name": boutique_name,
                "price": price,
                "video_link": video_link,
                "secret_key": secret_key,
                "custom_line_1": st.session_state["custom_line_1"],
                "custom_line_2": st.session_state["custom_line_2"],
                "custom_line_3": st.session_state["custom_line_3"]
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

                    # Extra: Ask for description (optional)
                    with st.expander("📌 Pinterest ਲਈ Description ਬਣਾਓ"):
                        user_description = st.text_area("ਰੇਟ ਮਿਟਾ ਕੇ description ਲਿਖੋ")
                        if user_description:
                            st.markdown("**📋 Final Output**")
                            st.code(f"₹{data['selling_price_inr']}\n{data['hidden_code']}\n{user_description}", language="text")
                            if st.button("📋 Copy All"):
                                copy_to_clipboard(f"₹{data['selling_price_inr']}\n{data['hidden_code']}\n{user_description}")
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
