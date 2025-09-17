#!/usr/bin/env python3
# Diffie-Hellman demo: correct scheme, wrong scheme (x^a), MITM, and brute-force discrete log.

import random
import math

def modexp(a, e, m):
    return pow(a, e, m)

# 1) Standard Diffie-Hellman functions
def dh_generate_secret(p, g):
    """Pick random secret x and compute g^x mod p."""
    x = random.randint(2, p-2)
    gx = modexp(g, x, p)
    return x, gx

def dh_shared_from_secret(their_gx, my_secret, p):
    """Compute (their_gx)^my_secret mod p == g^(their_secret * my_secret)"""
    return modexp(their_gx, my_secret, p)

# 2) Wrong scheme: parties send x^a mod p (secret^public) instead of g^x
def wrong_generate_sent_value(secret, a, p):
    """Send secret^a mod p (wrong scheme)"""
    return modexp(secret, a, p)

def wrong_derive_key(their_sent, my_secret, p):
    """If Alice tries to compute (their_sent)^my_secret -> their_secret^(a*my_secret)"""
    return modexp(their_sent, my_secret, p)

# 3) Simple brute-forcing discrete log (for demo only; works only for small p)
def discrete_log_bruteforce(g, h, p):
    """Find x such that g^x = h mod p by brute force (small p only)."""
    for x in range(0, p):
        if pow(g, x, p) == h:
            return x
    return None

# 4) MITM demonstration
def mitm_demo(p, g):
    print("\n--- MITM Demo on standard DH (no auth) ---")
    # Alice and Bob pick secrets
    a = random.randint(2, p-2)
    b = random.randint(2, p-2)
    A = pow(g, a, p)  # Alice sends A
    B = pow(g, b, p)  # Bob sends B

    # Eve intercepts; she chooses her own secrets ea, eb and substitutes:
    ea = random.randint(2, p-2)
    eb = random.randint(2, p-2)
    # Eve sends to Bob: E1 = g^ea (pretend this is from Alice)
    # Eve sends to Alice: E2 = g^eb (pretend this is from Bob)
    E_for_B = pow(g, ea, p)
    E_for_A = pow(g, eb, p)

    # Alice receives E_for_A and computes shared key = (E_for_A)^a
    K_ab_seen_by_A = pow(E_for_A, a, p)
    # Bob receives E_for_B and computes shared key = (E_for_B)^b
    K_ab_seen_by_B = pow(E_for_B, b, p)

    # Eve can compute both session keys:
    K_eve_with_A = pow(A, eb, p)   # note: Eve's eb used with Alice's real A to get shared with Alice
    K_eve_with_B = pow(B, ea, p)   # Eve's ea used with Bob's real B

    print("Alice's computed key (thinks it's shared with Bob):", K_ab_seen_by_A)
    print("Bob's computed key   (thinks it's shared with Alice):", K_ab_seen_by_B)
    print("Eve's key with Alice:", K_eve_with_A)
    print("Eve's key with Bob:  ", K_eve_with_B)
    print("Alice and Bob keys equal?", K_ab_seen_by_A == K_ab_seen_by_B)
    print("Eve can read/modify messages between them without solving DLP.")

# Demo main
if __name__ == "__main__":
    # Use small primes here for demonstration clarity; real DH uses huge safe primes.
    # p should be prime and g a generator modulo p (small for demo).
    p = 2087   # small prime (demo only)
    g = 2      # generator candidate

    print("=== Correct Diffie-Hellman ===")
    # Alice
    a_secret, A = dh_generate_secret(p, g)
    # Bob
    b_secret, B = dh_generate_secret(p, g)
    print("Alice secret (private):", a_secret)
    print("Alice sends A = g^a mod p:", A)
    print("Bob secret (private):", b_secret)
    print("Bob sends B = g^b mod p:", B)

    # Each computes shared key
    K_alice = dh_shared_from_secret(B, a_secret, p)   # B^a = g^(ab)
    K_bob   = dh_shared_from_secret(A, b_secret, p)   # A^b = g^(ab)
    print("Alice computed shared key:", K_alice)
    print("Bob   computed shared key:", K_bob)
    print("Keys equal?", K_alice == K_bob)

    # === Wrong scheme: send secret^a instead of g^secret ===
    print("\n=== Wrong Scheme: sending secret^a mod p (not secure/doesn't agree) ===")
    # pick small secrets (their secrets are not exponents of generator)
    alice_secret = random.randint(2, p-2)
    bob_secret   = random.randint(2, p-2)
    public_a = 5  # public exponent a (not generator)
    print("Alice's secret (as integer):", alice_secret)
    print("Bob's secret   (as integer):", bob_secret)
    sent_by_alice = wrong_generate_sent_value(alice_secret, public_a, p)  # alice sends alice_secret^a
    sent_by_bob   = wrong_generate_sent_value(bob_secret, public_a, p)
    print("Alice sends (alice_secret^a mod p):", sent_by_alice)
    print("Bob   sends (bob_secret^a mod p):", sent_by_bob)

    # If Alice tries to derive a key using Bob's sent value:
    k_a = wrong_derive_key(sent_by_bob, alice_secret, p)   # (bob_secret^a)^alice_secret = bob_secret^(a*alice_secret)
    # Bob:
    k_b = wrong_derive_key(sent_by_alice, bob_secret, p)
    print("Alice derived key (wrong_scheme):", k_a)
    print("Bob derived key   (wrong_scheme):", k_b)
    print("Do keys match? (usually no):", k_a == k_b)
    print("Unless secrets satisfy special relation, scheme fails to agree on same key.")

    # === MITM demonstration ===
    mitm_demo(p, g)

    # === Brute-force discrete log (small p demo) ===
    print("\n=== Brute-force discrete log demo (small p only) ===")
    # We'll show that for small p Eve can compute secret by brute force.
    # Use Alice's earlier A = g^a_secret mod p
    # Eve wants a_secret: solve g^x = A mod p
    found = discrete_log_bruteforce(g, A, p)
    if found is not None:
        print(f"Eve brute-forced discrete log: found a_secret = {found}, matches actual {a_secret}")
    else:
        print("Brute force failed (p too large for demo)")

    # Summary of security implications:
    print("\n--- Summary ---")
    print("1) Standard DH (send g^secret) -> Alice and Bob can agree on shared key g^(ab).")
    print("2) If instead they send secret^a (their secret raised to public exponent),")
    print("   they generally DON'T derive the same shared key -> scheme fails.")
    print("3) Without authentication, Eve can do MITM: intercept and form separate keys.")
    print("   This breaks confidentiality without solving discrete log.")
    print("4) Recovering secrets (discrete log) is infeasible for large secure primes,")
    print("   but trivial for small p (brute force) or weak parameters.")

