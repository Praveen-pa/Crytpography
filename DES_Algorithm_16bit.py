# DES decryption key generation in Python

# Shift schedule for each round
shift_schedule = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]

# PC1 and PC2 permutation tables
PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

def permute(bits, table):
    # Permutes bits according to the table
    return [bits[i -1] for i in table]

def left_shift(bits, n):
    # Left cyclic shift by n
    return bits[n:] + bits[:n]

def key_str_to_bits(key_str):
    # Converts binary string to list of bits (ints)
    return [int(b) for b in key_str]

def bits_to_str(bits):
    return ''.join(str(b) for b in bits)

def generate_round_keys(key64):
    # Convert key string to bits
    key_bits = key_str_to_bits(key64)
    # Initial permutation PC1
    key56 = permute(key_bits, PC1)
    # Split into C and D halves of 28 bits
    C = key56[:28]
    D = key56[28:]
    round_keys = []
    # Generate 16 round keys with left shifts
    for shift in shift_schedule:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        CD = C + D
        # Apply PC2 permutation
        round_key = permute(CD, PC2)
        round_keys.append(round_key)
    return round_keys

def main():
    key64 = input("Enter 64-bit key (binary, no spaces): ").strip()
    if len(key64) != 64 or any(c not in '01' for c in key64):
        print("Invalid key length or characters.")
        return
    round_keys = generate_round_keys(key64)
    print("\nDES Decryption Round Keys (K16 to K1):")
    for i in range(15, -1, -1):
        print(f"K{16 - i:02d}: {bits_to_str(round_keys[i])}")

if __name__ == "__main__":
    main()
