def generate_key(plaintext, key):
    key = key.lower()
    key_len = len(key)
    new_key = []
    j = 0
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            new_key.append(key[j % key_len])
            j += 1
        else:
            new_key.append(plaintext[i])
    return ''.join(new_key)

def encrypt(plaintext, key):
    key_full = generate_key(plaintext, key)
    ciphertext = []
    for p_char, k_char in zip(plaintext, key_full):
        if p_char.isalpha():
            base = ord('A') if p_char.isupper() else ord('a')
            shift = ord(k_char) - ord('a')
            encrypted_char = chr((ord(p_char) - base + shift) % 26 + base)
            ciphertext.append(encrypted_char)
        else:
            ciphertext.append(p_char)
    return ''.join(ciphertext)

# Example usage
plaintext = input("Enter the plaintext: ")
key = input("Enter the key: ")
ciphertext = encrypt(plaintext, key)
print("Encrypted message:", ciphertext)
