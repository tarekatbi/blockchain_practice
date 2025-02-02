import sys
import requests
import hashlib
import time

BASE_URL = "https://blockstream.info/api"

def sha256d(b: bytes) -> bytes:
    """Renvoie le double SHA256 de b."""
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def get_block_details(block_hash):
    url = f"{BASE_URL}/block/{block_hash}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Erreur lors de la récupération des détails du bloc {block_hash}: {e}")
        return None

def get_merkle_proof(txid):
    url = f"{BASE_URL}/tx/{txid}/merkle-proof"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Erreur lors de la récupération de la preuve de Merkle pour la transaction {txid}: {e}")
        return None

def compute_merkle_root(txid, proof):
    try:
        pos = proof["pos"]
        branch = proof["merkle"]
    except KeyError:
        print("La preuve récupérée n'est pas au bon format.")
        return None

    current = bytes.fromhex(txid)[::-1]

    for sibling_hex in branch:
        # Convertir le hash frère en bytes et inverser
        sibling = bytes.fromhex(sibling_hex)[::-1]
        if pos % 2 == 0:
            current = sha256d(current + sibling)
        else:
            current = sha256d(sibling + current)
        pos //= 2

    computed_root = current[::-1].hex()
    return computed_root

def main():
    if len(sys.argv) < 3:
        print("Usage : python app.py <block_hash> <txid>")
        sys.exit(1)
    
    block_hash = sys.argv[1].strip()
    txid = sys.argv[2].strip()

    print(f"Récupération des détails du bloc {block_hash}...")
    block_details = get_block_details(block_hash)
    if not block_details:
        sys.exit(1)
    
    block_merkle_root = block_details.get("merkle_root")
    if not block_merkle_root:
        print("La racine de l'arbre de Merkle n'a pas été trouvée dans les détails du bloc.")
        sys.exit(1)
    
    print(f"Racine de l'arbre de Merkle du bloc : {block_merkle_root}")

    print(f"Récupération de la preuve de Merkle pour la transaction {txid}...")
    proof = get_merkle_proof(txid)
    if not proof:
        sys.exit(1)
    
    print("Preuve de Merkle récupérée :")
    print(proof)

    computed_root = compute_merkle_root(txid, proof)
    if not computed_root:
        print("Impossible de calculer la racine de l'arbre de Merkle à partir de la preuve.")
        sys.exit(1)
    
    print(f"Racine calculée à partir de la preuve : {computed_root}")

    # Vérification
    if computed_root == block_merkle_root:
        print("\nLa preuve de Merkle est CORRECTE.")
    else:
        print("\nLa preuve de Merkle est INCORRECTE.")

if __name__ == "__main__":
    main()