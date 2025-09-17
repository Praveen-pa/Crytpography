import math

# Extended Euclidean Algorithm
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse exists")
    return x % m

# Example RSA keys
n = 3599         # modulus (p*q)
e = 31           # public key
d = 673          # leaked private key

print("Original Public Key: (e,n) =", (e, n))
print("Original Private Key: (d,n) =", (d, n))

# Attacker recovers phi(n) using leaked d
# e*d - 1 is divisible by phi(n)
kphi = e*d - 1   # must be a multiple of phi(n)

# Try to find phi(n) from divisors of kphi
def find_phi(kphi, e):
    # look for a divisor of kphi that gives integer phi
    for k in range(1, 1000):
        if (kphi % k) == 0:
            phi = kphi // k
            if math.gcd(e, phi) == 1:  # possible phi
                return phi
    return None

phi = find_phi(kphi, e)
print("Recovered phi(n):", phi)

# Factor n from phi
# phi = (p-1)(q-1) = pq - (p+q) + 1
# so p+q = n - phi + 1
sum_pq = n - phi + 1
# Solve quadratic x^2 - (p+q)x + pq = 0
discriminant = sum_pq**2 - 4*n
p = (sum_pq + int(discriminant**0.5)) // 2
q = n // p
print("Recovered factors: p =", p, ", q =", q)

# Now Bob tries to make a new key (e2, d2) with same n
e2 = 17
d2 = mod_inverse(e2, phi)
print("Bob's new keys: e2 =", e2, ", d2 =", d2)

# But attacker already knows p, q, phi, so can compute d2 too
d2_attacker = mod_inverse(e2, phi)
print("Attacker recomputes d2 =", d2_attacker)
