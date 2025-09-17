import math

# Extended Euclidean Algorithm
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return g, x, y

# Modular Inverse
def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse exists")
    return x % m

# Suppose we know this
n = 3599   # modulus
e = 31     # public exponent
plaintext_block = 59  # example plaintext with common factor (same as p)

# Step 1: Compute gcd
g = math.gcd(plaintext_block, n)

if g > 1:
    print(f"Found common factor! gcd({plaintext_block}, {n}) = {g}")
    p = g
    q = n // g
    print("Factors of n:", p, q)

    # Step 2: Compute phi(n)
    phi = (p - 1) * (q - 1)

    # Step 3: Compute private key d
    d = mod_inverse(e, phi)
    print("Private key (d, n):", (d, n))

    # Step 4: Test encryption/decryption
    message = 42
    ciphertext = pow(message, e, n)
    decrypted = pow(ciphertext, d, n)

    print("Original message:", message)
    print("Ciphertext:", ciphertext)
    print("Decrypted message:", decrypted)

else:
    print("No common factor found. System still secure.")
