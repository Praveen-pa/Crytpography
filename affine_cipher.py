import string
from math import gcd

# Convert char <-> number
def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

# Encryption
def affine_encrypt(text, a, b):
    if gcd(a, 26) != 1:
        raise ValueError(f"a={a} is not valid, gcd(a,26) != 1, encryption not invertible.")
    result = ""
    for char in text.upper():
        if char in string.ascii_uppercase:
            p = char_to_num(char)
            c = (a * p + b) % 26
            result += num_to_char(c)
        else:
            result += char  # keep non-letters as is
    return result

# Modular inverse using Extended Euclidean Algorithm
def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError("No modular inverse found.")

# Decryption
def affine_decrypt(ciphertext, a, b):
    if gcd(a, 26) != 1:
        raise ValueError(f"a={a} is not valid, gcd(a,26) != 1, decryption impossible.")
    a_inv = mod_inverse(a, 26)
    result = ""
    for char in ciphertext.upper():
        if char in string.ascii_uppercase:
            c = char_to_num(char)
            p = (a_inv * (c - b)) % 26
            result += num_to_char(p)
        else:
            result += char
    return result


# ------------------- TEST -------------------
if __name__ == "__main__":
    plaintext = "HELLOAFFINECIPHER"
    a, b = 5, 8   # valid keys since gcd(5,26)=1

    print("Plaintext:   ", plaintext)
    ciphertext = affine_encrypt(plaintext, a, b)
    print("Ciphertext:  ", ciphertext)
    decrypted = affine_decrypt(ciphertext, a, b)
    print("Decrypted:   ", decrypted)

    # Example of invalid key
    try:
        bad_a, bad_b = 2, 3
        print("\nTrying invalid key (a=2, b=3)...")
        test_cipher = affine_encrypt("TEST", bad_a, bad_b)
    except ValueError as e:
        print("Error:", e)
