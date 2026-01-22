import hashlib
import base64
import os

def derive_key(email: str, personal_seed: str, key_len: int = 32) -> bytes:
    h = hashlib.sha256((email + personal_seed).encode("utf-8")).digest()
    return h[:key_len]

def xor_stream(data: bytes, key: bytes) -> bytes:
    out = bytearray(len(data))
    klen = len(key)
    for i, b in enumerate(data):
        out[i] = b ^ key[i % klen]
    return bytes(out)

def encrypt_message(plaintext: str, key: bytes) -> str:
    nonce = os.urandom(16)
    payload = nonce + plaintext.encode("utf-8")
    ct = xor_stream(payload, key)
    return base64.b64encode(ct).decode("ascii")

def decrypt_message(ciphertext_b64: str, key: bytes) -> str:
    ct = base64.b64decode(ciphertext_b64.encode("ascii"))
    payload = xor_stream(ct, key)
    return payload[16:].decode("utf-8")

def demo():
    sender_email = "yevhenguriev69@gmail.com"
    receiver_email = "yevhen.huriev@hneu.net"

    shared_personal_seed = "HurievYevhen2004"
    message = "Зустрічаємося завтра о 15:00"

    print("=== Демонстрація симетричного шифрування повідомлень ===")
    print(f"[1] Відправник: {sender_email}")
    print(f"[2] Отримувач:  {receiver_email}")
    print("[3] Генерація спільного ключа з персональних даних (через SHA-256)...")

    key_sender = derive_key(sender_email, shared_personal_seed)
    key_receiver = derive_key(sender_email, shared_personal_seed)

    print(f"[4] Ключ згенеровано (довжина: {len(key_sender)} байт).")
    print(f"[5] Вихідне повідомлення: {message}")

    encrypted = encrypt_message(message, key_sender)
    print("[6] Повідомлення зашифровано (Base64-рядок):")
    print(encrypted)

    decrypted = decrypt_message(encrypted, key_receiver)
    print("[7] Отримувач розшифрував повідомлення:")
    print(decrypted)

    print("[8] Перевірка цілісності: ", "OK" if decrypted == message else "FAIL")

    print("\n=== Демонстрація підробки/неправильного ключа ===")
    wrong_key = derive_key(sender_email, "WrongSeed2004")
    try:
        wrong_decrypted = decrypt_message(encrypted, wrong_key)
        print("[9] Спроба розшифрувати неправильним ключем дала результат:")
        print(wrong_decrypted)
    except Exception as e:
        print("[9] Розшифрування неправильним ключем не вдалося:", str(e))

if __name__ == "__main__":
    demo()
