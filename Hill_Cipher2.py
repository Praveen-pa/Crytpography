MOD = 26

def mod_inverse(a):
    a %= MOD
    for x in range(1, MOD):
        if (a * x) % MOD == 1:
            return x
    return -1

def inverse_matrix(matrix):
    det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % MOD
    det_inv = mod_inverse(det)
    if det_inv == -1:
        raise ValueError("Matrix not invertible modulo 26")

    inv = [
        [( matrix[1][1] * det_inv) % MOD, (-matrix[0][1] * det_inv) % MOD],
        [(-matrix[1][0] * det_inv) % MOD, ( matrix[0][0] * det_inv) % MOD]
    ]

    for i in range(2):
        for j in range(2):
            if inv[i][j] < 0:
                inv[i][j] += MOD
    return inv

def multiply_matrices(a, b):
    result = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            total = 0
            for k in range(2):
                total += a[i][k] * b[k][j]
            result[i][j] = total % MOD
    return result

def char_to_num(c):
    return ord(c) - ord('A')

def print_matrix(mat, label="Matrix"):
    print(label)
    for row in mat:
        print("[ {:2d} {:2d} ]".format(row[0], row[1]))
    print()

def main():
    # Given plaintext matrix P
    plaintext = [
        [char_to_num('H'), char_to_num('L')],
        [char_to_num('E'), char_to_num('L')]
    ]

    # Given ciphertext matrix C
    ciphertext = [
        [char_to_num('Z'), char_to_num('S')],
        [char_to_num('K'), char_to_num('U')]
    ]

    print_matrix(plaintext, "Plaintext Matrix (P):")
    print_matrix(ciphertext, "Ciphertext Matrix (C):")

    # Compute inverse of plaintext matrix
    try:
        inverseP = inverse_matrix(plaintext)
    except ValueError as e:
        print("Error:", e)
        return

    print_matrix(inverseP, "Inverse of Plaintext Matrix (P^-1):")

    # Compute key matrix K = C * P^-1 mod 26
    key = multiply_matrices(ciphertext, inverseP)

    print_matrix(key, "Recovered Key Matrix (K = C * P^-1 mod 26):")

if __name__ == "__main__":
    main()
