import math

# RSA public key
e = 3        # small public exponent (example)
n = 9999991  # large modulus (secure against factoring)

# Alphabet encoding: A=0, B=1, ..., Z=25
alphabet = {chr(i+65): i for i in range(26)}
rev_alphabet = {v: k for k, v in alphabet.items()}

# Message to send
message = "HELLO"
print("Original message:", message)

# Encrypt each letter using RSA
cipher_blocks = []
for ch in message:
    m = alphabet[ch]
    c = pow(m, e, n)
    cipher_blocks.append(c)

print("Ciphertext blocks:", cipher_blocks)

# Attacker’s perspective:
# Recover plaintext by taking cube root (since m^e < n)
recovered = []
for c in cipher_blocks:
    m = round(c ** (1/e))  # approximate integer root
    recovered.append(rev_alphabet[m])

print("Recovered message (attack):", "".join(recovered))
