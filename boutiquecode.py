import urllib.parse

def generate_whatsapp_message(price_inr, product_code):
    final_price = price_inr + 700
    usd_price = round(final_price * 0.012, 2)

    video_link = input("Enter video/product link to include in WhatsApp message: ").strip()

    message = f"""Hi, I want to order this suit.

🔗 {video_link}

Price: ₹{final_price} / ${usd_price}

🇮🇳 India – Pay ₹{final_price}:
https://razorpay.me/@merapunjabisuit
(Free shipping within India)

🌍 International – Pay ${usd_price}:
https://paypal.me/parmjitkaur0069
(Shipping extra – we’ll confirm the amount after your order. Please pay shipping then.)

🧵 All suits are custom-made & take 5–20 days to prepare.

🆔 Product Code: {product_code}
"""

    encoded_msg = urllib.parse.quote(message)
    whatsapp_link = f"https://wa.me/917973567740?text={encoded_msg}"

    print("\n📦 WhatsApp Order Link (includes video, price & payment options):")
    print(whatsapp_link)

def encode():
    boutique_name = input("Enter boutique name (e.g., mehar_boutique01): ").strip()

    try:
        price = int(input("Enter original price (numbers only): ").strip())
    except ValueError:
        print("❌ Invalid price input. Please enter numbers only.")
        return

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

    encoded_price = str(price * 786)
    price_encoded = '-'.join(list(encoded_price))  # Correct way to split digits with dashes

    full_code = f"{encoded_name}__{price_encoded}"
    hidden_code = full_code[::-1]

    print("\n✅ Encoded Output:")
    print("🔐 Hidden Code:", hidden_code)
    print("💰 Original Price: Rs.", price)
    print("🛍️ Selling Price: Rs.", price + 700, f"/ ${round((price + 700) * 0.012, 2)}")

    generate_whatsapp_message(price, hidden_code)

if __name__ == "__main__":
    encode()
