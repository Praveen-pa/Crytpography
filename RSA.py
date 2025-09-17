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

# RSA parameters
e = 31
n = 3599

# Step 1: Factorize n
p, q = 59, 61
phi = (p-1)*(q-1)

# Step 2: Find private key d
d = mod_inverse(e, phi)

print("Public key (e,n):", (e,n))
print("p =", p, "q =", q)
print("phi(n) =", phi)
print("Private key (d,n):", (d,n))
