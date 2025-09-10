import string
import random

def generate_cipher_key():
    alphabet = list(string.ascii_lowercase)
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def encrypt(plaintext, key):
    ciphertext = ""
    for char in plaintext.lower():
        if char in key:
            ciphertext += key[char]
        else:
            ciphertext += char
    return ciphertext

def decrypt(ciphertext, key):
    reverse_key = {v: k for k, v in key.items()}
    plaintext = ""
    for char in ciphertext:
        if char in reverse_key:
            plaintext += reverse_key[char]
        else:
            plaintext += char
    return plaintext

# Example usage
cipher_key = generate_cipher_key()
message = "cryptography is fun!"
ciphered = encrypt(message, cipher_key)
deciphered = decrypt(ciphered, cipher_key)

print("Cipher Key:", cipher_key)
print("Original:", message)
print("Encrypted:", ciphered)
print("Decrypted:", deciphered)
