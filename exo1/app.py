import requests
import sys
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    """Crée et configure une session avec une stratégie de retry."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_block_transactions(block_hash, base_url="https://blockstream.info/api"):
    session = get_session()
    
    block_url = f"{base_url}/block/{block_hash}"
    try:
        r = session.get(block_url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des détails du bloc: {e}")
        sys.exit(1)
    
    block_details = r.json()
    tx_count = block_details.get("tx_count", 0)
    print(f"Le bloc {block_hash} contient {tx_count} transactions.")
    
    transactions = []
    start_index = 0
    page = 1
    
    while start_index < tx_count:
        if start_index == 0:
            url = f"{base_url}/block/{block_hash}/txs"
        else:
            url = f"{base_url}/block/{block_hash}/txs/{start_index}"
            
        print(f"Fetching page {page} (start_index = {start_index})")
        try:
            r = session.get(url, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération de la page {page}: {e}")
            break
        
        txs = r.json()
        count = len(txs)
        print(f"Page {page}: {count} transactions récupérées")
        if count == 0:
            break
        
        transactions.extend(txs)
        start_index += count
        page += 1
        time.sleep(0.2)
    
    print(f"Total des transactions récupérées: {len(transactions)}")
    return transactions

def transaction_total_value(tx):
    total = 0
    for output in tx.get("vout", []):
        total += output.get("value", 0)
    return total

def find_transaction_with_max_value(transactions):
    max_tx = None
    max_value = 0
    for tx in transactions:
        total_value = transaction_total_value(tx)
        if total_value > max_value:
            max_value = total_value
            max_tx = tx
    return max_tx, max_value

def main():
    if len(sys.argv) < 2:
        print("Usage : python app.py <block_hash>")
        sys.exit(1)
    
    block_hash = sys.argv[1]
    if len(block_hash) != 64:
        print("Attention : le block_hash semble invalide (doit contenir 64 caractères hexadécimaux).")
    
    print("Récupération des transactions pour le bloc :", block_hash)
    transactions = get_block_transactions(block_hash)
    
    if not transactions:
        print("Aucune transaction trouvée pour le bloc", block_hash)
        sys.exit(1)
    
    print("Analyse des transactions pour déterminer celle avec le plus gros montant échangé...")
    max_tx, max_value = find_transaction_with_max_value(transactions)
    
    if max_tx:
        print("\nTransaction avec le plus gros montant échangé :")
        print("TXID                :", max_tx.get("txid"))
        print("Valeur totale échangée :", max_value, "satoshis")
    else:
        print("Aucune transaction n'a été trouvée.")

if __name__ == "__main__":
    main()