# DES key schedule with separated C-part and D-part in Python

shift_schedule = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]

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
    return [bits[i - 1] for i in table]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def key_str_to_bits(key_str):
    return [int(b) for b in key_str]

def bits_to_str(bits):
    return ''.join(str(b) for b in bits)

def generate_round_keys(key64):
    key_bits = key_str_to_bits(key64)
    key56 = permute(key_bits, PC1)
    C = key56[:28]
    D = key56[28:]
    round_keys = []
    for shift in shift_schedule:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        CD = C + D
        subkey = permute(CD, PC2)
        round_keys.append((subkey[:24], subkey[24:]))  # Split into C-part and D-part
    return round_keys

def main():
    key64 = input("Enter 64-bit binary key (no spaces): ").strip()
    if len(key64) != 64 or any(ch not in '01' for ch in key64):
        print("Invalid key length or characters.")
        return
    round_keys = generate_round_keys(key64)
    print("\nDES Subkeys (C-part | D-part):")
    for i, (c_part, d_part) in enumerate(round_keys, 1):
        print(f"K{i:02d}: {bits_to_str(c_part)} | {bits_to_str(d_part)}")

if __name__ == "__main__":
    main()
