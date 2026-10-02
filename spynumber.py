import re
import urllib.parse
import webbrowser

import phonenumbers
from phonenumbers import (
    geocoder,
    carrier,
    timezone,
    PhoneNumberType
)


# ==============================
# WARNA TERMINAL
# ==============================

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"


# ==============================
# BANNER
# ==============================

def banner():
    print(CYAN + """
╔══════════════════════════════════════╗
║          SPYNUMBER v3                ║
║        OSINT PHONE CHECKER           ║
╠══════════════════════════════════════╣
║  Public information checker          ║
╚══════════════════════════════════════╝
""" + RESET)


# ==============================
# NORMALISASI NOMOR
# ==============================

def normalize_number(number):
    number = re.sub(r"[\s\-().]", "", number)

    if number.startswith("08"):
        return "+62" + number[1:]

    if number.startswith("62"):
        return "+" + number

    return number


# ==============================
# CEK METADATA
# ==============================

def get_phone_info(number):

    try:
        parsed = phonenumbers.parse(number, None)

        valid = phonenumbers.is_valid_number(parsed)
        possible = phonenumbers.is_possible_number(parsed)

        country_code = parsed.country_code

        region = geocoder.description_for_number(
            parsed,
            "id"
        )

        operator = carrier.name_for_number(
            parsed,
            "id"
        )

        timezones = timezone.time_zones_for_number(
            parsed
        )

        number_type = phonenumbers.number_type(parsed)

        type_names = {
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE: "Fixed line",
            PhoneNumberType.FIXED_LINE_OR_MOBILE:
                "Fixed line or mobile",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.TOLL_FREE:
                "Toll free",
            PhoneNumberType.PREMIUM_RATE:
                "Premium rate",
            PhoneNumberType.PAGER:
                "Pager",
            PhoneNumberType.UAN:
                "UAN",
            PhoneNumberType.VOICEMAIL:
                "Voicemail",
        }

        number_type_name = type_names.get(
            number_type,
            "Unknown"
        )

        return {
            "valid": valid,
            "possible": possible,
            "country_code": country_code,
            "region": region or "Tidak tersedia",
            "operator": operator or "Tidak tersedia",
            "timezone": ", ".join(timezones)
                if timezones
                else "Tidak tersedia",
            "type": number_type_name
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==============================
# TAMPILKAN METADATA
# ==============================

def show_metadata(number):

    info = get_phone_info(number)

    print("\n" + CYAN + "PHONE INFORMATION" + RESET)
    print("-" * 40)

    if "error" in info:

        print(
            RED
            + "Error: "
            + info["error"]
            + RESET
        )

        return

    valid_text = (
        GREEN + "True" + RESET
        if info["valid"]
        else RED + "False" + RESET
    )

    possible_text = (
        GREEN + "True" + RESET
        if info["possible"]
        else RED + "False" + RESET
    )

    print("Number       :", number)
    print("Valid        :", valid_text)
    print("Possible     :", possible_text)
    print(
        "Country code : +"
        + str(info["country_code"])
    )
    print("Region       :", info["region"])
    print("Operator     :", info["operator"])
    print("Timezone     :", info["timezone"])
    print("Type         :", info["type"])


# ==============================
# BUAT QUERY
# ==============================

def search_queries(number):

    return [
        f'"{number}" penipu',
        f'"{number}" penipuan',
        f'"{number}" scam',
        f'"{number}" fraud',
        f'"{number}" WhatsApp'
    ]


# ==============================
# GOOGLE SEARCH
# ==============================

def google_search(number):

    queries = search_queries(number)

    print("\n" + CYAN + "GOOGLE OSINT" + RESET)
    print("-" * 40)

    for i, query in enumerate(queries, 1):

        url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote(query)
        )

        print(f"{i}. {query}")
        webbrowser.open(url)


# ==============================
# BING SEARCH
# ==============================

def bing_search(number):

    queries = search_queries(number)

    print("\n" + CYAN + "BING OSINT" + RESET)
    print("-" * 40)

    for i, query in enumerate(queries, 1):

        url = (
            "https://www.bing.com/search?q="
            + urllib.parse.quote(query)
        )

        print(f"{i}. {query}")
        webbrowser.open(url)


# ==============================
# TAMPILKAN URL TANPA MEMBUKA
# ==============================

def show_search_urls(number):

    queries = search_queries(number)

    print("\n" + CYAN + "PUBLIC SEARCH URL" + RESET)
    print("-" * 40)

    for i, query in enumerate(queries, 1):

        google_url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote(query)
        )

        bing_url = (
            "https://www.bing.com/search?q="
            + urllib.parse.quote(query)
        )

        print(f"\n[{i}] {query}")
        print("Google:")
        print(google_url)
        print("Bing:")
        print(bing_url)


# ==============================
# INPUT NOMOR
# ==============================

def input_number():

    number = input(
        "\nMasukkan nomor: "
    ).strip()

    normalized = normalize_number(number)

    print(
        "\nNomor normal : "
        + GREEN
        + normalized
        + RESET
    )

    return normalized


# ==============================
# MENU
# ==============================

def menu():

    number = None

    while True:

        print("\n" + CYAN + "=" * 40 + RESET)
        print(CYAN + "           SPYNUMBER v3" + RESET)
        print(CYAN + "=" * 40 + RESET)

        print("""
1. Cek nomor
2. Lihat metadata nomor
3. Google OSINT
4. Bing OSINT
5. Tampilkan URL pencarian
6. Ganti nomor
0. Keluar
""")

        choice = input(
            "Pilih menu: "
        ).strip()

        # --------------------------
        # CEK NOMOR
        # --------------------------

        if choice == "1":

            number = input_number()

            show_metadata(number)

        # --------------------------
        # METADATA
        # --------------------------

        elif choice == "2":

            if number is None:
                number = input_number()

            show_metadata(number)

        # --------------------------
        # GOOGLE
        # --------------------------

        elif choice == "3":

            if number is None:
                number = input_number()

            google_search(number)

        # --------------------------
        # BING
        # --------------------------

        elif choice == "4":

            if number is None:
                number = input_number()

            bing_search(number)

        # --------------------------
        # URL
        # --------------------------

        elif choice == "5":

            if number is None:
                number = input_number()

            show_search_urls(number)

        # --------------------------
        # GANTI NOMOR
        # --------------------------

        elif choice == "6":

            number = input_number()

        # --------------------------
        # KELUAR
        # --------------------------

        elif choice == "0":

            print(
                "\n"
                + GREEN
                + "SPYNUMBER selesai."
                + RESET
            )

            break

        else:

            print(
                RED
                + "\nPilihan tidak tersedia."
                + RESET
            )


# ==============================
# START
# ==============================

if __name__ == "__main__":
    banner()
    menu()