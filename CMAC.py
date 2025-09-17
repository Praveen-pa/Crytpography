from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes

def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')

def int_to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, byteorder='big')

def xor_bytes(a: bytes, b: bytes) -> bytes:
    la = len(a); lb = len(b)
    assert la == lb
    return bytes(x ^ y for x, y in zip(a, b))

def generate_cmac_subkeys_from_cipher_encrypt_fn(enc_fn, block_size_bytes: int):
    """
    enc_fn: function that takes a single block (bytes length block_size_bytes) and returns encryption (bytes)
    block_size_bytes: block size in bytes (8 for 64-bit, 16 for 128-bit)
    Returns tuple (K1_bytes, K2_bytes)
    """
    block_size_bits = block_size_bytes * 8
    mask = (1 << block_size_bits) - 1

    # 1) Encrypt zero block to get L
    zero_block = b'\x00' * block_size_bytes
    L_bytes = enc_fn(zero_block)
    L = bytes_to_int(L_bytes)

    # Choose Rb constant (least-significant byte value) per RFC 4493 / NIST CMAC:
    # - for 64-bit block: Rb = 0x1B
    # - for 128-bit block: Rb = 0x87
    if block_size_bits == 64:
        Rb = 0x1B
    elif block_size_bits == 128:
        Rb = 0x87
    else:
        raise ValueError("This helper supports only 64-bit or 128-bit block sizes for standard CMAC constants.")

    # Rb is XORed into the least-significant byte of the shifted value when MSB was 1.
    # Represent Rb as integer aligned to the block (LSB position).
    Rb_int = Rb

    def dbl(x: int) -> int:
        """Multiply x by 'x' (i.e., left shift by 1 in GF(2^b)), then conditionally XOR Rb if overflowed."""
        msb_set = (x >> (block_size_bits - 1)) & 1  # extract MSB before shift
        x_shl = ((x << 1) & mask)
        if msb_set:
            x_shl ^= Rb_int
        return x_shl

    K1 = dbl(L)
    K2 = dbl(K1)

    return int_to_bytes(K1, block_size_bytes), int_to_bytes(K2, block_size_bytes), L_bytes, Rb

# --- Demonstrations using AES (128-bit) and DES (64-bit) ---
def aes_enc_block_factory(key: bytes):
    cipher = AES.new(key, AES.MODE_ECB)
    def enc(block: bytes) -> bytes:
        return cipher.encrypt(block)
    return enc

def des_enc_block_factory(key: bytes):
    cipher = DES.new(key, DES.MODE_ECB)
    def enc(block: bytes) -> bytes:
        return cipher.encrypt(block)
    return enc

if __name__ == "__main__":
    # AES-128 example (128-bit block)
    aes_key = get_random_bytes(16)
    aes_enc = aes_enc_block_factory(aes_key)
    K1_aes, K2_aes, L_aes, Rb_aes = generate_cmac_subkeys_from_cipher_encrypt_fn(aes_enc, 16)
    print("AES (128-bit block) example")
    print("L = E_K(0^128)      :", L_aes.hex())
    print("Rb (constant byte)  : 0x{:02x}".format(Rb_aes))
    print("K1                  :", K1_aes.hex())
    print("K2                  :", K2_aes.hex())
    print()

    # DES example (64-bit block)
    des_key = get_random_bytes(8)
    des_enc = des_enc_block_factory(des_key)
    K1_des, K2_des, L_des, Rb_des = generate_cmac_subkeys_from_cipher_encrypt_fn(des_enc, 8)
    print("DES (64-bit block) example")
    print("L = E_K(0^64)       :", L_des.hex())
    print("Rb (constant byte)  : 0x{:02x}".format(Rb_des))
    print("K1                  :", K1_des.hex())
    print("K2                  :", K2_des.hex())
    print()

    # Quick sanity: show how K1 is derived from L (bit-level)
    def show_bits(label, bts):
        return ' '.join(f"{byte:02x}" for byte in bts)

    print("Sanity check (AES):")
    print(" L   :", show_bits("L", L_aes))
    print(" K1  :", show_bits("K1", K1_aes))
    print(" K2  :", show_bits("K2", K2_aes))
