# Програма порівняльного аналізу шифрів Цезаря та Віженера

class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift
        self.alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
        
    def encrypt(self, text):
        result = ''
        for char in text.upper():
            if char in self.alphabet:
                old_index = self.alphabet.index(char)
                new_index = (old_index + self.shift) % len(self.alphabet)
                result += self.alphabet[new_index]
            else:
                result += char
        return result
    
    def decrypt(self, text):
        result = ''
        for char in text.upper():
            if char in self.alphabet:
                old_index = self.alphabet.index(char)
                new_index = (old_index - self.shift) % len(self.alphabet)
                result += self.alphabet[new_index]
            else:
                result += char
        return result


class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()
        self.alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
        
    def encrypt(self, text):
        result = ''
        key_index = 0
        for char in text.upper():
            if char in self.alphabet:
                text_index = self.alphabet.index(char)
                key_char = self.key[key_index % len(self.key)]
                key_shift = self.alphabet.index(key_char)
                new_index = (text_index + key_shift) % len(self.alphabet)
                result += self.alphabet[new_index]
                key_index += 1
            else:
                result += char
        return result
    
    def decrypt(self, text):
        result = ''
        key_index = 0
        for char in text.upper():
            if char in self.alphabet:
                text_index = self.alphabet.index(char)
                key_char = self.key[key_index % len(self.key)]
                key_shift = self.alphabet.index(key_char)
                new_index = (text_index - key_shift) % len(self.alphabet)
                result += self.alphabet[new_index]
                key_index += 1
            else:
                result += char
        return result


def generate_caesar_key(birthdate):
    digit_sum = sum(int(d) for d in birthdate if d.isdigit())
    return digit_sum


def analyze_cipher(name, original, encrypted, key_info):
    print(f"\n{'='*60}")
    print(f"Аналіз шифру: {name}")
    print(f"{'='*60}")
    print(f"Оригінальний текст: {original}")
    print(f"Зашифрований текст: {encrypted}")
    print(f"Ключ: {key_info}")
    print(f"Довжина оригіналу: {len(original)} символів")
    print(f"Довжина зашифрованого: {len(encrypted)} символів")
    
    letters_only = ''.join(c for c in encrypted if c.isalpha())
    unique_chars = len(set(letters_only))
    print(f"Унікальних символів: {unique_chars}")
    print(f"Складність ключа: {'Низька (одне число)' if isinstance(key_info, int) else f'Середня (слово з {len(str(key_info))} літер)'}")


def main():
    print("ПОРІВНЯЛЬНИЙ АНАЛІЗ КЛАСИЧНИХ ШИФРІВ")
    print("="*60)
    
    surname = input("Введіть ваше прізвище (кирилицею): ")
    birthdate = input("Введіть дату народження (ДД.ММ.РРРР): ")
    test_text = input("Введіть текст для шифрування: ")
    
    caesar_shift = generate_caesar_key(birthdate)
    vigenere_key = surname
    
    print(f"\nЗгенеровані ключі:")
    print(f"Шифр Цезаря - зсув: {caesar_shift} (сума цифр дати)")
    print(f"Шифр Віженера - ключ: {vigenere_key}")
    
    caesar = CaesarCipher(caesar_shift)
    vigenere = VigenereCipher(vigenere_key)
    
    caesar_encrypted = caesar.encrypt(test_text)
    vigenere_encrypted = vigenere.encrypt(test_text)
    
    analyze_cipher("Цезар", test_text, caesar_encrypted, caesar_shift)
    analyze_cipher("Віженер", test_text, vigenere_encrypted, vigenere_key)
    
    print(f"\n{'='*60}")
    print("ПОРІВНЯЛЬНА ТАБЛИЦЯ")
    print(f"{'='*60}")
    print(f"{'Параметр':<30} {'Цезар':<15} {'Віженер':<15}")
    print(f"{'-'*60}")
    print(f"{'Довжина ключа':<30} {1:<15} {len(vigenere_key):<15}")
    print(f"{'Складність злому':<30} {'Дуже низька':<15} {'Низька':<15}")
    print(f"{'Варіантів ключа':<30} {33:<15} {'~10^'+str(len(vigenere_key)):<15}")
    print(f"{'Періодичність шифру':<30} {'Ні':<15} {f'{len(vigenere_key)} літер':<15}")
    
    caesar_decrypted = caesar.decrypt(caesar_encrypted)
    vigenere_decrypted = vigenere.decrypt(vigenere_encrypted)
    
    print(f"\n{'='*60}")
    print("ПЕРЕВІРКА РОЗШИФРУВАННЯ")
    print(f"{'='*60}")
    print(f"Цезар розшифровано: {caesar_decrypted}")
    print(f"Віженер розшифровано: {vigenere_decrypted}")
    print(f"Цезар вірно: {'ТАК' if caesar_decrypted.upper() == test_text.upper() else 'НІ'}")
    print(f"Віженер вірно: {'ТАК' if vigenere_decrypted.upper() == test_text.upper() else 'НІ'}")


if __name__ == "__main__":
    main()
