def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1

def affine_encrypt_char(ch, a, b):
    if ch.isalpha():
        is_upper = ch.isupper()
        base = ord('A') if is_upper else ord('a')
        x = ord(ch) - base
        e = (a * x + b) % 26
        return chr(e + base)
    else:
        return ch

def affine_decrypt_char(ch, a, b):
    if ch.isalpha():
        is_upper = ch.isupper()
        base = ord('A') if is_upper else ord('a')
        a_inv = mod_inverse(a)
        if a_inv == -1:
            return '?'
        y = ord(ch) - base
        d = (a_inv * (y - b + 26)) % 26
        return chr(d + base)
    else:
        return ch

def encrypt(plaintext, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("'a' must be coprime with 26")
    return ''.join(affine_encrypt_char(ch, a, b) for ch in plaintext)

def decrypt(ciphertext, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("'a' must be coprime with 26")
    return ''.join(affine_decrypt_char(ch, a, b) for ch in ciphertext)

# Example usage
a = int(input("Enter value for 'a' (must be coprime to 26): "))
b = int(input("Enter value for 'b': "))
plaintext = input("Enter the plaintext (letters only): ")

try:
    ciphertext = encrypt(plaintext, a, b)
    print("Encrypted:", ciphertext)
    decrypted = decrypt(ciphertext, a, b)
    print("Decrypted:", decrypted)
except ValueError as e:
    print(e)
