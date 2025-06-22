import re
import urllib.parse


def generate_whatsapp_message(price_inr, product_code):
    final_price = price_inr + 700
    usd_price = round(final_price * 0.012, 2)


    message = f"""

Price: ₹{final_price} / ${usd_price}

🇮🇳 India – Pay ₹{final_price}:
https://razorpay.me/@merapunjabisuit
(Free shipping within India)

🌍 International – Pay ${usd_price}:
https://paypal.me/parmjitkaur0069
(Shipping extra – we’ll contact you)

🧵 All suits are custom-made & take 5–20 days to prepare.

🆔 Product Code: {product_code}
"""

    encoded_msg = urllib.parse.quote(message)
    whatsapp_link = f"https://wa.me/917973567740?text={encoded_msg}"

    print("\n🚞 WhatsApp Order Link (includes video, price & payment options):")
    print(whatsapp_link)


def decode():
    encoded_input = input("Enter encoded & reversed code: ").strip()
    un_reversed = encoded_input[::-1]

    # Handle incorrect format: convert single "_" to "__" if only one exists
    if '__' not in un_reversed:
        parts = un_reversed.split('_')
        if len(parts) == 2:
            un_reversed = un_reversed.replace('_', '__', 1)
        else:
            print("Invalid code format.")
            return

    name_part, price_part = un_reversed.split('__', 1)

    # Decode boutique name
    decoded_name = ''
    name_codes = name_part.split('-')
    i = 0
    while i < len(name_codes):
        code = name_codes[i]
        if code == '_':
            decoded_name += '_'
            i += 1
        elif code == '0' and i + 1 < len(name_codes) and name_codes[i + 1].isdigit():
            # Handle sequences like 0-1 → "01"
            decoded_name += code + name_codes[i + 1]
            i += 2
        elif code.isdigit():
            num = int(code)
            if 1 <= num <= 26:
                decoded_name += chr(num + 96)
            else:
                decoded_name += code
            i += 1
        else:
            decoded_name += code
            i += 1


    # Extract original price
    price_digits = ''.join(re.findall(r'\d+', price_part))
    try:
        price_candidate = int(price_digits)
        if price_candidate % 786 == 0:
            original_price = price_candidate // 786
            selling_price = original_price + 700
            usd_price = round(selling_price * 0.012, 2)
            
        else:
            raise ValueError("Price encoding mismatch.")
    except:
        print("Price – Unknown")
        return

    print("\nDecoded Output:")
    print("Boutique Name:", decoded_name)
    print(f"Original Price: ₹{original_price}")
    print(f"Selling Price: ₹{selling_price} / ${usd_price}")
    generate_whatsapp_message(original_price, encoded_input)


if __name__ == "__main__":
    decode()