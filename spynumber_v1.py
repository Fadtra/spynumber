

import urllib.parse
import webbrowser

nomor = input("Masukkan nomor: ").strip()

if nomor.startswith("0"):
    nomor_int = "+62" + nomor[1:]
else:
    nomor_int = nomor

print("\nNomor:", nomor_int)
print("\nMembuka pencarian publik...")

queries = [
    f'"{nomor_int}" penipu',
    f'"{nomor_int}" penipuan',
    f'"{nomor_int}" scam',
    f'"{nomor_int}" fraud'
]

for query in queries:
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    print(url)
    webbrowser.open(url)
