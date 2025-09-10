def mod_inverse(a, m=26):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1

def decrypt_char(ch, a, b):
    if ch.isalpha():
        a_inv = mod_inverse(a)
        if a_inv == -1:
            return '?'
        y = ord(ch.upper()) - ord('A')
        p = (a_inv * (y - b + 26)) % 26
        return chr(p + ord('A'))
    else:
        return ch

def solve_key(c1, c2, p1, p2):
    diff_p = (p1 - p2) % 26
    diff_c = (c1 - c2) % 26
    inv_diff_p = mod_inverse(diff_p)
    if inv_diff_p == -1:
        return None, None
    a = (diff_c * inv_diff_p) % 26
    b = (c1 - a * p1) % 26
    return a, b

# Example ciphertext and known plaintext letter mappings
ciphertext = "BUBUBUBUBUBUBUBUBUBU"
# Most frequent ciphertext letters 'B' and 'U'
c1 = ord('B') - ord('A')
c2 = ord('U') - ord('A')
# Most frequent plaintext letters e(4) and t(19)
p1 = ord('E') - ord('A')
p2 = ord('T') - ord('A')

a, b = solve_key(c1, c2, p1, p2)
if a is None:
    print("Unable to find valid 'a'. Decryption not possible.")
else:
    print(f"Recovered Key: a = {a}, b = {b}")
    plaintext = ''.join(decrypt_char(ch, a, b) for ch in ciphertext)
    print("Decrypted Text:", plaintext)
