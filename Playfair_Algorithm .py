import string

SIZE = 5

def generate_matrix(key):
    key = key.lower().replace('j','i')
    matrix_list = []
    used = [False]*26
    used[ord('j')-ord('a')] = True   # treat j as i

    for ch in key:
        if ch.isalpha():
            idx = ord(ch)-ord('a')
            if not used[idx]:
                matrix_list.append(ch)
                used[idx] = True

    for i in range(26):
        if not used[i]:
            matrix_list.append(chr(i+ord('a')))

    # Convert to 5x5 matrix
    matrix = [matrix_list[i*SIZE:(i+1)*SIZE] for i in range(SIZE)]
    return matrix

def prepare_text(input_text):
    input_text = input_text.lower()
    formatted = []
    for ch in input_text:
        if ch.isalpha():
            if ch == 'j':
                formatted.append('i')
            else:
                formatted.append(ch)
    # build digraphs with 'x' for repeated letters and pad end if odd
    output = []
    i = 0
    while i < len(formatted):
        a = formatted[i]
        b = formatted[i+1] if i+1 < len(formatted) else 'x'
        if a == b:
            output.append(a)
            output.append('x')
            i += 1
        else:
            output.append(a)
            output.append(b)
            i += 2
    if len(output) % 2 != 0:
        output.append('x')
    return ''.join(output)

def find_position(matrix, ch):
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j] == ch:
                return i, j
    return None, None

def encrypt(plaintext, matrix):
    ciphertext = []
    i = 0
    while i < len(plaintext):
        a, b = plaintext[i], plaintext[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:   # same row
            ciphertext.append(matrix[r1][(c1+1)%SIZE])
            ciphertext.append(matrix[r2][(c2+1)%SIZE])
        elif c1 == c2: # same column
            ciphertext.append(matrix[(r1+1)%SIZE][c1])
            ciphertext.append(matrix[(r2+1)%SIZE][c2])
        else:          # rectangle
            ciphertext.append(matrix[r1][c2])
            ciphertext.append(matrix[r2][c1])
        i += 2
    return ''.join(ciphertext)

def print_matrix(matrix):
    print("Playfair Matrix:")
    for row in matrix:
        print(' '.join(row))

# Example usage
key = input("Enter keyword: ")
plaintext = input("Enter plaintext: ")
matrix = generate_matrix(key)
print_matrix(matrix)
formatted = prepare_text(plaintext)
ciphertext = encrypt(formatted, matrix)
print("Formatted Plaintext:", formatted)
print("Encrypted Ciphertext:", ciphertext)
