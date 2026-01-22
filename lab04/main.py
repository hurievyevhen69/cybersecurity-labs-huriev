import hashlib
import os

MOD = 1000007
MUL = 7

def sha256_bytes(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def sha256_hex_of_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def derive_private_key(name: str, dob_ddmmyyyy: str, secret: str) -> int:
    h = hashlib.sha256((name + dob_ddmmyyyy + secret).encode("utf-8")).hexdigest()
    return int(h, 16)

def derive_public_key(private_key: int) -> int:
    return (private_key * MUL) % MOD

def sign_file(path: str, private_key: int) -> str:
    doc_hash = sha256_bytes(open(path, "rb").read())
    key_bytes = private_key.to_bytes(32, "big", signed=False)
    sig = bytes(a ^ b for a, b in zip(doc_hash, key_bytes))
    return sig.hex()

def verify_file(path: str, signature_hex: str, public_key: int, private_key_hint: int | None = None) -> bool:
    current_hash = sha256_bytes(open(path, "rb").read())
    sig = bytes.fromhex(signature_hex)
    if private_key_hint is None:
        return False
    if derive_public_key(private_key_hint) != public_key:
        return False
    key_bytes = private_key_hint.to_bytes(32, "big", signed=False)
    recovered_hash = bytes(a ^ b for a, b in zip(sig, key_bytes))
    return recovered_hash == current_hash

def save_keys(private_key: int, public_key: int, priv_path: str = "private.key", pub_path: str = "public.key") -> None:
    with open(priv_path, "w", encoding="utf-8") as f:
        f.write(str(private_key))
    with open(pub_path, "w", encoding="utf-8") as f:
        f.write(str(public_key))

def load_key_int(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        return int(f.read().strip())

def demo(document_path: str) -> None:
    name = "Гур'єв Євген Романович"
    dob = "07102004"
    secret = "соломка"

    priv = derive_private_key(name, dob, secret)
    pub = derive_public_key(priv)
    save_keys(priv, pub)

    sig = sign_file(document_path, priv)

    ok = verify_file(document_path, sig, pub, private_key_hint=priv)
    print("Підпис ДІЙСНИЙ" if ok else "Підпис ПІДРОБЛЕНИЙ")

    tampered_path = document_path + ".tampered"
    with open(document_path, "rb") as f:
        data = f.read()
    with open(tampered_path, "wb") as f:
        f.write(data + b"\nTAMPERED\n")

    ok2 = verify_file(tampered_path, sig, pub, private_key_hint=priv)
    print("Підпис ДІЙСНИЙ" if ok2 else "Підпис ПІДРОБЛЕНИЙ")

    fake_priv = derive_private_key(name, dob, "інше_слово")
    fake_sig = sign_file(document_path, fake_priv)

    ok3 = verify_file(document_path, fake_sig, pub, private_key_hint=priv)
    print("Підпис ДІЙСНИЙ" if ok3 else "Підпис ПІДРОБЛЕНИЙ")

if __name__ == "__main__":
    path = input("Вкажіть шлях до файлу документа: ").strip()
    if not os.path.isfile(path):
        raise SystemExit("Файл не знайдено")
    demo(path)
