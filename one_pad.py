import random
import string

# --- Generate a random key stream ---
def generate_key(length):
    return [random.randint(0, 25) for _ in range(length)]

# --- Encrypt ---
def otp_vigenere_encrypt(plaintext, key):
    ciphertext = []
    for i, char in enumerate(plaintext.upper()):
        if char in string.ascii_uppercase:
            shift = key[i]
            encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            ciphertext.append(encrypted_char)
        else:
            ciphertext.append(char)  # keep non-letters as is
    return "".join(ciphertext)

# --- Decrypt ---
def otp_vigenere_decrypt(ciphertext, key):
    plaintext = []
    for i, char in enumerate(ciphertext.upper()):
        if char in string.ascii_uppercase:
            shift = key[i]
            decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            plaintext.append(decrypted_char)
        else:
            plaintext.append(char)
    return "".join(plaintext)


# ------------------- TEST -------------------
if __name__ == "__main__":
    message = "HELLOCRYPTO"
    key = generate_key(len(message))   # random key stream same length as message

    print("Message:   ", message)
    print("Key:       ", key)

    ciphertext = otp_vigenere_encrypt(message, key)
    print("Encrypted: ", ciphertext)

    decrypted = otp_vigenere_decrypt(ciphertext, key)
    print("Decrypted: ", decrypted)
