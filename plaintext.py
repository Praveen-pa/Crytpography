import numpy as np

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Convert text <-> numbers
def text_to_numbers(text):
    return [ALPHABET.index(c.upper()) for c in text if c.isalpha()]

def numbers_to_text(numbers):
    return "".join(ALPHABET[n % 26] for n in numbers)

# Modular inverse for matrices
def mod_matrix_inv(matrix, modulus):
    det = int(round(np.linalg.det(matrix)))  # determinant
    det_inv = pow(det, -1, modulus)  # modular inverse of determinant
    matrix_modinv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_modinv % modulus

# Hill cipher encryption
def hill_encrypt(plaintext, key_matrix):
    n = key_matrix.shape[0]
    nums = text_to_numbers(plaintext)
    # pad if necessary
    if len(nums) % n != 0:
        nums += [0] * (n - len(nums) % n)
    ciphertext = []
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        cipher_block = np.dot(block, key_matrix) % 26
        ciphertext.extend(cipher_block)
    return numbers_to_text(ciphertext)

# Hill cipher decryption
def hill_decrypt(ciphertext, key_matrix):
    n = key_matrix.shape[0]
    key_inv = mod_matrix_inv(key_matrix, 26)
    nums = text_to_numbers(ciphertext)
    plaintext = []
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        plain_block = np.dot(block, key_inv) % 26
        plaintext.extend(plain_block)
    return numbers_to_text(plaintext)

# Known-plaintext attack (solve for key matrix)
def hill_known_plaintext_attack(plaintext_blocks, ciphertext_blocks, n):
    """
    plaintext_blocks: list of n-length plaintext strings
    ciphertext_blocks: list of corresponding ciphertext strings
    """
    P = np.array([text_to_numbers(block) for block in plaintext_blocks]).T  # n x n
    C = np.array([text_to_numbers(block) for block in ciphertext_blocks]).T
    P_inv = mod_matrix_inv(P, 26)
    K = np.dot(P_inv, C) % 26
    return K.astype(int)

# ------------------- TEST -------------------
if __name__ == "__main__":
    # Example key (2x2)
    K = np.array([[3, 3],
                  [2, 5]])
    plaintext = "HELP"
    ciphertext = hill_encrypt(plaintext, K)
    print("Original plaintext:", plaintext)
    print("Encrypted ciphertext:", ciphertext)
    
    decrypted = hill_decrypt(ciphertext, K)
    print("Decrypted text:", decrypted)

    # Known-plaintext attack
    # Suppose attacker knows plaintext "HE" -> ciphertext "RI" and "LP" -> "FP"
    pt_blocks = ["HE", "LP"]
    ct_blocks = [ciphertext[:2], ciphertext[2:]]
    recovered_key = hill_known_plaintext_attack(pt_blocks, ct_blocks, n=2)
    print("Recovered key matrix:\n", recovered_key)

    # Verify recovered key
    decrypted_with_recovered = hill_decrypt(ciphertext, recovered_key)
    print("Decrypted with recovered key:", decrypted_with_recovered)
