import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np

def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def encrypt_button_clicked():
    text_to_encrypt = text_entry_encrypt.get("1.0", tk.END).strip()
    if not text_to_encrypt:
        result_label_encrypted.config(text="Wprowadź tekst do zaszyfrowania.")
        return
    shift_text = shift_entry_encrypt.get()
    if not shift_text:
        result_label_encrypted.config(text="Podaj klucz przesunięcia.")
        return
    try:
        shift = int(shift_text)
    except ValueError:
        result_label_encrypted.config(text="Klucz przesunięcia musi być liczbą całkowitą.")
        return
    encrypted_text = caesar_cipher(text_to_encrypt, shift)
    text_entry_encoded.delete(1.0, tk.END)
    text_entry_encoded.insert(tk.END, encrypted_text)
    result_label_encrypted.config(text="Tekst został zaszyfrowany.")

def encode_button_clicked():
    image_path = image_entry_encode.get()
    if not image_path:
        result_label_encode.config(text="Wybierz obraz do zakodowania.")
        return
    text_to_encode = text_entry_encoded.get("1.0", tk.END).strip()
    if not text_to_encode:
        result_label_encode.config(text="Wprowadź tekst do zakodowania.")
        return
    shift_text = shift_entry_encrypt.get()
    if not shift_text:
        result_label_encode.config(text="Podaj klucz przesunięcia.")
        return
    try:
        shift = int(shift_text)
    except ValueError:
        result_label_encode.config(text="Klucz przesunięcia musi być liczbą całkowitą.")
        return
    encode_text(image_path, text_to_encode, shift)

def decode_button_clicked():
    encoded_image_path = image_entry_decode.get()
    if not encoded_image_path:
        result_label_decode.config(text="Wybierz obraz do odkodowania.")
        return
    decoded_text = decode_text(encoded_image_path)
    result_label_decode.config(text="Odkodowany tekst: " + decoded_text)

def encode_text(image_path, text, shift):
    image = Image.open(image_path)
    text_binary = ''.join(format(ord(char), '08b') for char in text)
    required_length = image.width * image.height * 3
    if len(text_binary) > required_length:
        raise ValueError("Tekst jest zbyt długi, aby zakodować go w tym obrazie.")
    elif len(text_binary) < required_length:
        text_binary += '0' * (required_length - len(text_binary))
    pixel_values = np.array(image)
    text_index = 0
    for y in range(image.height):
        for x in range(image.width):
            if text_index < len(text_binary):
                for c in range(3):
                    pixel_values[y][x][c] &= ~1
                    pixel_values[y][x][c] |= int(text_binary[text_index])
                    text_index += 1
            else:
                break
        if text_index >= len(text_binary):
            break
    encoded_image = Image.fromarray(pixel_values)
    encoded_image.save("encoded_image.png")
    result_label_encode.config(text="Tekst został pomyślnie zakodowany w obrazie.")



def decode_text(encoded_image_path):
    encoded_image = Image.open(encoded_image_path)
    pixel_values = np.array(encoded_image)
    text_binary = ""
    for y in range(encoded_image.height):
        for x in range(encoded_image.width):
            for c in range(3):
                text_binary += str(pixel_values[y][x][c] & 1)
    text = ""
    for i in range(0, len(text_binary), 8):
        byte = text_binary[i:i+8]
        if byte:
            text += chr(int(byte, 2))
            if text.endswith('\x00'):  # Zakończ, jeśli napotkano znak pustego ciągu
                break
    return text

def select_image():
    image_path = filedialog.askopenfilename()
    image_entry_encode.delete(0, tk.END)
    image_entry_encode.insert(0, image_path)
    image_entry_decode.delete(0, tk.END)
    image_entry_decode.insert(0, image_path)

#okno
root = tk.Tk()
root.title("Steganografia")

#szyfrowanie
text_label_encrypt = tk.Label(root, text="Wprowadź tekst do zaszyfrowania:")
text_label_encrypt.grid(row=0, column=0, padx=5, pady=5)
text_entry_encrypt = tk.Text(root, width=50, height=5)
text_entry_encrypt.grid(row=0, column=1, padx=5, pady=5)

shift_label_encrypt = tk.Label(root, text="Podaj klucz przesunięcia:")
shift_label_encrypt.grid(row=1, column=0, padx=5, pady=5)
shift_entry_encrypt = tk.Entry(root)
shift_entry_encrypt.grid(row=1, column=1, padx=5, pady=5)

encrypt_button = tk.Button(root, text="Zaszyfruj tekst", command=encrypt_button_clicked)
encrypt_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

text_label_encoded = tk.Label(root, text="Wprowadź zaszyfrowany tekst:")
text_label_encoded.grid(row=3, column=0, padx=5, pady=5)
text_entry_encoded = tk.Text(root, width=50, height=5)
text_entry_encoded.grid(row=3, column=1, padx=5, pady=5)

#kodowanie i dekodowanie
image_label_encode = tk.Label(root, text="Wybierz obraz do zakodowania:")
image_label_encode.grid(row=4, column=0, padx=5, pady=5)
image_entry_encode = tk.Entry(root, width=50)
image_entry_encode.grid(row=4, column=1, padx=5, pady=5)
image_button_encode = tk.Button(root, text="Wybierz", command=select_image)
image_button_encode.grid(row=4, column=2, padx=5, pady=5)

encode_button = tk.Button(root, text="Zakoduj tekst w obrazie", command=encode_button_clicked)
encode_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

image_label_decode = tk.Label(root, text="Wybierz obraz do odkodowania:")
image_label_decode.grid(row=6, column=0, padx=5, pady=5)
image_entry_decode = tk.Entry(root, width=50)
image_entry_decode.grid(row=6, column=1, padx=5, pady=5)
image_button_decode = tk.Button(root, text="Wybierz", command=select_image)
image_button_decode.grid(row=6, column=2, padx=5, pady=5)

decode_button = tk.Button(root, text="Odkoduj tekst z obrazu", command=decode_button_clicked)
decode_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

result_label_decode = tk.Label(root, text="")
result_label_decode.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

result_label_encode = tk.Label(root, text="")
result_label_encode.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

result_label_encrypted = tk.Label(root, text="")
result_label_encrypted.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
