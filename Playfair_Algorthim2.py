def generate_key_matrix(key):
    key = key.upper().replace('J', 'I')
    used = set()
    matrix = []
    for ch in key:
        if 'A' <= ch <= 'Z' and ch not in used:
            used.add(ch)
    for ch in key:
        if ch in used:
            matrix.append(ch)
            used.remove(ch)

    # Fill remaining letters except J
    for ch in (chr(i) for i in range(ord('A'), ord('Z') + 1)):
        if ch != 'J' and ch not in matrix:
            matrix.append(ch)
    # Convert to 5x5 matrix
    key_matrix = [matrix[i*5:(i+1)*5] for i in range(5)]
    return key_matrix

def find_position(matrix, ch):
    if ch == 'J':
        ch = 'I'
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j
    return None, None

def decrypt_pair(matrix, a, b):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_message(matrix, ciphertext):
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i].upper()
        b = ciphertext[i+1].upper()
        if a == 'J':
            a = 'I'
        if b == 'J':
            b = 'I'
        plaintext += decrypt_pair(matrix, a, b)
    return plaintext

def main():
    keyword = "PLAYFAIR"
    ciphertext = (
        "KXJEYUREBEZWEHEWRYTUHEYFS"
        "KREHEGOYFIWTTTUOLKSYCAJPO"
        "BOTEIZONTXBYBNTGONEYCUZWR"
        "GDSONSXBOUYWRHEBAAHYUSEDQ"
    )
    print("Decrypting Playfair Cipher...\n")
    matrix = generate_key_matrix(keyword)
    decrypted_text = decrypt_message(matrix, ciphertext)
    print("Decrypted Text:")
    print(decrypted_text)

if __name__ == "__main__":
    main()
