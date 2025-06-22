import streamlit as st
import urllib.parse
import re

st.title("🧵 WhatsApp ਆਰਡਰ ਟੂਲ")

# --- ENCODING FUNCTION ---
def encode_boutique(boutique_name, price, video_link):
    try:
        price = int(price)
    except ValueError:
        return None, "ਰੇਟ ਭਰੋ (ਸਿਰਫ਼ ਨੰਬਰ)"

    name_encoded = []
    for ch in boutique_name:
        if ch.isalpha():
            num = ord(ch.lower()) - ord('a') + 1
            name_encoded.append(str(num))
        elif ch.isdigit():
            name_encoded.append(ch)
        elif ch == '_':
            name_encoded.append('_')

    encoded_name = '-'.join(name_encoded)
    encoded_price = '-'.join(list(str(price * 786)))
    full_code = f"{encoded_name}__{encoded_price}"
    hidden_code = full_code[::-1]

    final_price = price + 700
    usd_price = round(final_price * 0.012, 2)
    message = f"""Hi, I want to order this suit.\n🔗 {video_link}\n🇮🇳 India – Pay ₹{final_price}: https://razorpay.me/@merapunjabisuit (Free delivery in India)\n🌍 International – Pay ${usd_price}: https://paypal.me/parmjitkaur0069 (Delivery charges extra.)\n🧵 Delivery time: 5–20 days.\n🆔 Product Code: {hidden_code}

---

ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਜੀ, ਮੈਂ ਇਹ ਸੂਟ ਆਰਡਰ ਕਰਨਾ ਹੈ।\n🔗 {video_link}\n🇮🇳 ਭਾਰਤ ਲਈ – ₹{final_price}: https://razorpay.me/@merapunjabisuit (ਭਾਰਤ ਵਿੱਚ ਮੁਫ਼ਤ ਡਿਲਿਵਰੀ)\n🌍 ਇੰਟਰਨੈਸ਼ਨਲ – ${usd_price}: https://paypal.me/parmjitkaur0069 (ਡਿਲਿਵਰੀ ਚਾਰਜ ਵੱਖਰੇ ਹੋਣਗੇ।)\n🧵 ਆਰਡਰ ਤੋਂ ਬਾਅਦ 5–20 ਦਿਨ ਲੱਗਣਗੇ।\n🆔 ਕੋਡ: {hidden_code}"""

    encoded_msg = urllib.parse.quote(message)
    whatsapp_link = f"https://wa.me/917973567740?text={encoded_msg}"
    return hidden_code, whatsapp_link

# --- DECODING FUNCTION ---
def decode_code(hidden_code):
    try:
        reversed_code = hidden_code[::-1]
        encoded_name, encoded_price = reversed_code.split("__")
        name_parts = encoded_name.split('-')
        decoded_name = ""
        for part in name_parts:
            if part == '_':
                decoded_name += '_'
            elif part.isdigit():
                n = int(part)
                if 1 <= n <= 26:
                    decoded_name += chr(ord('a') + n - 1)
                else:
                    decoded_name += part

        decoded_price = int(''.join(encoded_price.split('-'))) // 786
        final_price = decoded_price + 700
        usd_price = round(final_price * 0.012, 2)

        message = f"""Hi, I want to order this suit.\n🔗 [Product Link Here]\nPrice: ₹{final_price} / ${usd_price}\n🇮🇳 India – Pay ₹{final_price}: https://razorpay.me/@merapunjabisuit (Free delivery in India)\n🌍 International – Pay ${usd_price}: https://paypal.me/parmjitkaur0069 (Delivery charges extra.)\n🧵 Delivery time: 5–20 days.\n🆔 Product Code: {hidden_code}

---

ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਜੀ, ਮੈਂ ਇਹ ਸੂਟ ਆਰਡਰ ਕਰਨਾ ਹੈ।\n🔗 [Product Link Here]\nਭੁਗਤਾਨ: ₹{final_price} / ${usd_price}\n🇮🇳 ਭਾਰਤ ਲਈ – ₹{final_price}: https://razorpay.me/@merapunjabisuit (ਭਾਰਤ ਵਿੱਚ ਮੁਫ਼ਤ ਡਿਲਿਵਰੀ)\n🌍 ਇੰਟਰਨੈਸ਼ਨਲ – ${usd_price}: https://paypal.me/parmjitkaur0069 (ਡਿਲਿਵਰੀ ਚਾਰਜ ਵੱਖਰੇ ਹੋਣਗੇ।)\n🧵 ਆਰਡਰ ਤੋਂ ਬਾਅਦ 5–20 ਦਿਨ ਲੱਗਣਗੇ।\n🆔 ਕੋਡ: {hidden_code}"""

        encoded_msg = urllib.parse.quote(message)
        whatsapp_link = f"https://wa.me/917973567740?text={encoded_msg}"

        return decoded_name, decoded_price, whatsapp_link
    except:
        return None, None, "ਕੋਡ ਗਲਤ ਹੈ। ਦੁਬਾਰਾ ਜਾਂਚੋ।"

# --- CLEAN DESCRIPTION ---
def clean_description(raw_desc):
    desc_no_price = re.sub(r"(?i)(price|rs|₹)[^\n]*", "", raw_desc)
    desc_no_brand = re.sub(r"^[A-Z\- ]{2,}\n", "", desc_no_price.strip(), flags=re.MULTILINE)
    return desc_no_brand.strip()

# --- UI ---
st.header("ਪੈਸੇ ਹੀ ਪੈਸੇ")
with st.form("encode_form"):
    col1, col2 = st.columns(2)
    with col1:
        boutique = st.text_input("ਬੁਟੀਕ ਦਾ ਨਾਂ", placeholder="e.g., mehar_boutique01")
    with col2:
        price = st.text_input("ਅਸਲੀ ਰੇਟ", placeholder="e.g., 3800")
    video_link = st.text_input("ਵੀਡੀਓ ਜਾਂ ਫੋਟੋ pinterest 'ਤੇ ਪਾ ਆਓ, ਉਸਤੋਂ ਬਾਅਦ ਉਸਦਾ ਲਿੰਕ ਇਥੇ paste ਕਰੋ")
    encode_submit = st.form_submit_button("ਲਿੰਕ ਬਣਾਓ")

    if encode_submit:
        code, link = encode_boutique(boutique, price, video_link)
        if code:
            st.success(f"🆔 ਕੋਡ ਬਣ ਗਿਆ: {code}")
            st.code(link, language="")
            st.info("ਇਸ ਲਿੰਕ ਨੂੰ ਹੁਣ ਤੁਸੀਂ ਆਪਣੀ Pin edit ਕਰਕੇ ਉਥੇ ਪਾ ਆਓ, ਜਿਵੇਂ ਹੀ ਕੋਈ ਲਿੰਕ 'ਤੇ ਕਲਿੱਕ ਕਰੇਗਾ , ਤੁਹਾਡੇ whatsapp 'ਤੇ order ਦੇ ਜਾਵੇਗਾ ਤੇ bank 'ਚ ਪੈਸੇ ਪਾ ਜਾਵੇਗਾ।")

            if st.checkbox("ਕੀ ਤੁਸੀਂ Pinterest ਲਈ ਬਣੀ - ਬਣਾਈ Title ਤੇ description ਵੀ ਲੈਣਾ ਚਾਹੋਗੇ?", value=True):
                full_desc = st.text_area("ਆਪਣਾ ਸਾਰਾ ਉਤਪਾਦ ਵੇਰਵਾ ਇੱਥੇ ਪਾਓ", height=200)
                if full_desc:
                    clean_desc = clean_description(full_desc)
                    selling_price = int(price) + 700
                    st.markdown("---")
                    st.subheader("📋 ਤਿਆਰ ਕੀਤੀ ਹੋਈ ਪੋਸਟ:")
                    st.code(f"₹{selling_price}\n{code}\n{clean_desc}")
                    st.success("✅ ਇਸਨੂੰ ਕਾਪੀ ਕਰੋ ਤੇ Pin edit ਕਰਕੇ Description 'ਚ ਪਾ ਦਿਓ")
        else:
            st.error(link)

st.header("ਕੋਡ ਤੋਂ ਪਤਾ ਲਗਾਓ ਬੁਟੀਕ ਦਾ ਨਾਂ ਤੇ ਰੇਟ")
with st.form("decode_form"):
    hidden_code = st.text_input("ਲੰਮੇ ਅੱਖਰਾਂ ਵਾਲਾ ਕੋਡ ਭਰੋ")
    decode_submit = st.form_submit_button("ਦੱਸੋ ਕਿਸਦਾ ਸੂਟ ਆ ਇਹ ਤੇ ਕਿੰਨੇ ਦਾ ਹੈ")

    if decode_submit:
        name, orig_price, link = decode_code(hidden_code)
        if name:
            st.success(f"ਬੁਟੀਕ: {name}")
            st.info(f"ਬਣਿਆ ਹੋਇਆ ਰੇਟ: ₹{orig_price+700} / ${round((orig_price+700)*0.012, 2)}")
            st.code(link, language="")
        else:
            st.error(link)
