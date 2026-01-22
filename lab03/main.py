from PIL import Image
import os

def hide_message(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    width, height = img.size
    
    message_bytes = message.encode('utf-8')
    message_length = len(message_bytes)
    length_bytes = message_length.to_bytes(4, byteorder='big')
    full_data = length_bytes + message_bytes
    
    bits = ''.join(format(byte, '08b') for byte in full_data)
    
    max_bits = len(pixels) * 3
    if len(bits) > max_bits:
        raise ValueError("Повідомлення завелике")
    
    new_pixels = []
    bit_index = 0
    
    for pixel in pixels:
        r, g, b = pixel
        if bit_index < len(bits):
            r = (r & ~1) | int(bits[bit_index])
            bit_index += 1
        if bit_index < len(bits):
            g = (g & ~1) | int(bits[bit_index])
            bit_index += 1
        if bit_index < len(bits):
            b = (b & ~1) | int(bits[bit_index])
            bit_index += 1
        new_pixels.append((r, g, b))
    
    new_img = Image.new('RGB', (width, height))
    new_img.putdata(new_pixels)
    new_img.save(output_path, 'PNG')

def extract_message(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    
    bits = []
    for pixel in pixels:
        bits.append(pixel[0] & 1)
        bits.append(pixel[1] & 1)
        bits.append(pixel[2] & 1)
    
    length_bytes = []
    for i in range(0, 32, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        length_bytes.append(byte)
    message_length = int.from_bytes(bytes(length_bytes), byteorder='big')
    
    message_bits = bits[32:32 + message_length * 8]
    message_bytes = []
    for i in range(0, len(message_bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(message_bits):
                byte = (byte << 1) | message_bits[i + j]
        message_bytes.append(byte)
    
    return bytes(message_bytes).decode('utf-8')

print("Створення тестового зображення...")
img = Image.new('RGB', (400, 300))
pixels = []
for y in range(300):
    for x in range(400):
        r = (x * 255) // 400
        g = (y * 255) // 300
        b = ((x + y) * 255) // 700
        pixels.append((r, g, b))
img.putdata(pixels)
img.save('original.png')
print("Тестове зображення створено")

personal_message = "Віталій Шевченко, ФОП, Київ, Україна, Факультет інформаційних технологій"

print("Приховування повідомлення...")
hide_message('original.png', personal_message, 'stego.png')
print("Повідомлення сховано")

print("Витягування повідомлення...")
extracted = extract_message('stego.png')
print("Повідомлення витягнуто")

print(f"\nОригінальне повідомлення: {personal_message}")
print(f"Витягнуте повідомлення: {extracted}")
print(f"Співпадає: {personal_message == extracted}")

original = Image.open('original.png')
stego = Image.open('stego.png')

orig_pixels = list(original.getdata())
stego_pixels = list(stego.getdata())

differences = sum(1 for o, s in zip(orig_pixels, stego_pixels) if o != s)

print(f"\nАналіз змін:")
print(f"Розмір оригіналу: {original.size}")
print(f"Розмір стего: {stego.size}")
print(f"Змінено пікселів: {differences} з {len(orig_pixels)}")
print(f"Відсоток змін: {(differences / len(orig_pixels) * 100):.2f}%")

orig_size = os.path.getsize('original.png')
stego_size = os.path.getsize('stego.png')
print(f"\nРозмір файлу оригіналу: {orig_size} байт")
print(f"Розмір файлу стего: {stego_size} байт")
print(f"Різниця: {stego_size - orig_size} байт")
