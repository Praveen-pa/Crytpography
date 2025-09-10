MOD = 26

def matrix_multiply(key, pair):
    # Multiply 2x2 key matrix with 2x1 pair vector modulo 26
    res0 = (key[0][0] * pair[0] + key[0][1] * pair[1]) % MOD
    res1 = (key[1][0] * pair[0] + key[1][1] * pair[1]) % MOD
    return [res0, res1]

def mod_inverse(a):
    a %= MOD
    for x in range(1, MOD):
        if (a * x) % MOD == 1:
            return x
    return -1

def inverse_key(key):
    # Compute inverse of 2x2 matrix modulo 26
    det = (key[0][0] * key[1][1] - key[0][1] * key[1][0]) % MOD
    if det < 0:
        det += MOD
    inv_det = mod_inverse(det)
    if inv_det == -1:
        raise ValueError("Key matrix is not invertible")
    inv_key = [
        [( key[1][1] * inv_det) % MOD, (-key[0][1] * inv_det) % MOD],
        [(-key[1][0] * inv_det) % MOD, ( key[0][0] * inv_det) % MOD]
    ]
    for i in range(2):
        for j in range(2):
            if inv_key[i][j] < 0:
                inv_key[i][j] += MOD
    return inv_key

def preprocess(text):
    # Remove non-alpha, uppercase, and replace J with I
    clean = []
    for ch in text:
        if ch.isalpha():
            c = ch.upper()
            if c == 'J':
                c = 'I'
            clean.append(c)
    if len(clean) % 2 != 0:
        clean.append('X')  # pad if length is odd
    return clean

def encrypt_hill(message, key):
    encrypted = []
    for i in range(0, len(message), 2):
        pair = [ord(message[i]) - ord('A'), ord(message[i+1]) - ord('A')]
        res = matrix_multiply(key, pair)
        encrypted.append(chr(res[0] + ord('A')))
        encrypted.append(chr(res[1] + ord('A')))
    return ''.join(encrypted)

def decrypt_hill(ciphertext, key):
    inv_key = inverse_key(key)
    decrypted = []
    length = len(ciphertext)
    if length % 2 != 0:
        print("Warning: ciphertext length is odd; ignoring last character for decryption.")
        length -= 1
    for i in range(0, length, 2):
        pair = [ord(ciphertext[i]) - ord('A'), ord(ciphertext[i+1]) - ord('A')]
        res = matrix_multiply(inv_key, pair)
        decrypted.append(chr(res[0] + ord('A')))
        decrypted.append(chr(res[1] + ord('A')))
    return ''.join(decrypted)


def main():
    text = "meet me at the usual place at ten rather than eight oclock"
    key = [[9, 4], [5, 7]]

    clean = preprocess(text)
    clean_text = ''.join(clean)
    print("Cleaned Message:", clean_text)

    encrypted = encrypt_hill(clean, key)
    print("Encrypted Text:")
    print(encrypted)

    # Decrypt given ciphertext from example
    ciphertext = "KCLUBGUBDKXIJAFKXZQLNDWSJAGRLJCKYUVCDPVQGVQMLYHUG"
    decrypted = decrypt_hill(ciphertext, key)
    print("\nDecrypted Text from given ciphertext:")
    print(decrypted)

if __name__ == "__main__":
    main()