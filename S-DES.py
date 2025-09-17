# -------------------------------
# S-DES Implementation (CTR Mode)
# -------------------------------

# Permutations
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8  = [6, 3, 7, 4, 8, 5, 10, 9]
P4  = [2, 4, 3, 1]
IP  = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP  = [4, 1, 2, 3, 2, 3, 4, 1]

# S-Boxes
S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

# --- Helper functions ---
def permute(bits, table):
    return [bits[i-1] for i in table]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def sbox_lookup(bits, sbox):
    row = (bits[0] << 1) | bits[3]
    col = (bits[1] << 1) | bits[2]
    val = sbox[row][col]
    return [ (val >> 1) & 1 , val & 1 ]

# --- Key Generation ---
def generate_keys(key10):
    key10 = [int(b) for b in key10]
    p10 = permute(key10, P10)
    left, right = p10[:5], p10[5:]
    left, right = left_shift(left,1), left_shift(right,1)
    K1 = permute(left+right, P8)
    left, right = left_shift(left,2), left_shift(right,2)
    K2 = permute(left+right, P8)
    return K1, K2

# --- Fk Function ---
def fk(bits, subkey):
    left, right = bits[:4], bits[4:]
    expanded = permute(right, EP)
    xored = xor(expanded, subkey)
    s0 = sbox_lookup(xored[:4], S0)
    s1 = sbox_lookup(xored[4:], S1)
    p4 = permute(s0+s1, P4)
    left = xor(left, p4)
    return left + right

# --- S-DES Encrypt one block ---
def sdes_encrypt_block(block8, K1, K2):
    bits = [int(b) for b in block8]
    bits = permute(bits, IP)
    bits = fk(bits, K1)
    bits = bits[4:] + bits[:4]   # swap
    bits = fk(bits, K2)
    bits = permute(bits, IP_INV)
    return bits

# --- CTR Mode ---
def ctr_encrypt_decrypt(text, key10, counter_start):
    """Same function works for both encryption and decryption in CTR mode."""
    K1, K2 = generate_keys(key10)
    blocks = [text[i:i+8] for i in range(0,len(text),8)]
    counter = int(counter_start, 2)
    result = []
    for block in blocks:
        counter_bits = [int(b) for b in format(counter, "08b")]
        keystream = sdes_encrypt_block(counter_bits, K1, K2)
        block_bits = [int(b) for b in block]
        out_bits = xor(block_bits, keystream)
        result.extend(out_bits)
        counter += 1
    return ''.join(str(b) for b in result)

# --- Test with given data ---
if __name__ == "__main__":
    key = "0111111101"
    plaintext = "000000010000001000000100"
    counter_start = "00000000"

    print("Plaintext :", plaintext)
    ciphertext = ctr_encrypt_decrypt(plaintext, key, counter_start)
    print("Ciphertext:", ciphertext)
    decrypted = ctr_encrypt_decrypt(ciphertext, key, counter_start)
    print("Decrypted :", decrypted)
