import sys
import requests
import time
from collections import defaultdict

BASE_URL = "https://blockstream.info/api"

def get_block_hash(height):
    url = f"{BASE_URL}/block-height/{height}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        block_hash = r.text.strip()
        return block_hash
    except Exception as e:
        print(f"Erreur lors de la récupération du hash pour la hauteur {height}: {e}")
        return None

def get_block_transactions(block_hash):

    transactions = []
    start_index = 0
    page = 1

    while True:
        if start_index == 0:
            url = f"{BASE_URL}/block/{block_hash}/txs"
        else:
            url = f"{BASE_URL}/block/{block_hash}/txs/{start_index}"
        print(f"  Récupération de la page {page} (start_index = {start_index})")
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"  Erreur lors de la récupération des transactions pour le bloc {block_hash} à l'index {start_index}: {e}")
            break

        txs = r.json()
        if not txs:
            break

        transactions.extend(txs)
        if len(txs) < 25:
            break

        start_index += len(txs)
        page += 1
        time.sleep(0.2)  

    return transactions

def main():
    if len(sys.argv) < 3:
        print("Usage : python app.py <h1> <h2>")
        sys.exit(1)
    try:
        h1 = int(sys.argv[1])
        h2 = int(sys.argv[2])
    except ValueError:
        print("Veuillez fournir deux entiers.")
        sys.exit(1)
    if h1 > h2:
        print("h1 doit être inférieur ou égal à h2")
        sys.exit(1)

    # Dictionnaire pour compter les apparitions de chaque adresse
    address_counts = defaultdict(int)

    for height in range(h1, h2 + 1):
        print(f"\nTraitement du bloc de hauteur {height}...")
        block_hash = get_block_hash(height)
        if not block_hash:
            print(f"  Bloc à la hauteur {height} introuvable.")
            continue
        transactions = get_block_transactions(block_hash)
        print(f"  Nombre de transactions dans le bloc {height} : {len(transactions)}")
        for tx in transactions:
            vouts = tx.get("vout", [])
            for vout in vouts:
                address = vout.get("scriptpubkey_address")
                if address:
                    address_counts[address] += 1

    if not address_counts:
        print("Aucune adresse trouvée dans l'intervalle spécifié.")
        sys.exit(0)

    max_address = None
    max_count = 0
    for address, count in address_counts.items():
        if count > max_count:
            max_count = count
            max_address = address

    print("\nAdresse Bitcoin la plus fréquente dans l'intervalle :")
    print(f"Adresse : {max_address}")
    print(f"Nombre d'apparitions : {max_count}")

if __name__ == "__main__":
    main()