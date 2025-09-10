SIZE = 5

matrix = [
    ['M', 'F', 'H', 'I', 'K'],
    ['U', 'N', 'O', 'P', 'Q'],
    ['Z', 'V', 'W', 'X', 'Y'],
    ['E', 'L', 'A', 'R', 'G'],
    ['D', 'S', 'T', 'B', 'C']
]

def find_position(ch):
    if ch == 'J':
        ch = 'I'
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j] == ch:
                return i, j
    return None, None

def encrypt_pair(a, b):
    r1, c1 = find_position(a)
    r2, c2 = find_position(b)
    if r1 == r2:
        return matrix[r1][(c1 + 1) % SIZE] + matrix[r2][(c2 + 1) % SIZE]
    elif c1 == c2:
        return matrix[(r1 + 1) % SIZE][c1] + matrix[(r2 + 1) % SIZE][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def prepare_text(text):
    clean = []
    for ch in text:
        if ch.isalpha():
            c = ch.upper()
            if c == 'J':
                c = 'I'
            clean.append(c)
    pairs = []
    i = 0
    while i < len(clean):
        a = clean[i]
        b = ''
        if i + 1 < len(clean):
            b = clean[i+1]
        else:
            b = 'X'
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a,b))
            i += 2
    return pairs

def encrypt_message(text):
    pairs = prepare_text(text)
    encrypted = ''
    for a, b in pairs:
        encrypted += encrypt_pair(a, b)
    return encrypted

def main():
    message = "Must see you over Cadogan West. Coming at once."
    print("Original Message:\n", message, "\n")
    encrypted_text = encrypt_message(message)
    print("Encrypted Message:")
    print(encrypted_text)

if __name__ == "__main__":
    main()
