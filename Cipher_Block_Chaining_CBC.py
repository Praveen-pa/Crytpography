BLOCK_SIZE = 8

def xor_bytes(block, key):
    return bytes([b ^ k for b, k in zip(block, key)])

def xor_blocks(in1, in2):
    return bytes([a ^ b for a, b in zip(in1, in2)])

def cbc_encrypt(plaintext, key, iv):
    ciphertext = b""
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        # XOR plaintext block with prev ciphertext (or iv)
        xored = xor_blocks(block, prev)
        # Encrypt xored block with key (using XOR here as placeholder)
        encrypted = xor_bytes(xored, key)
        ciphertext += encrypted
        prev = encrypted
    return ciphertext

def cbc_decrypt(ciphertext, key, iv):
    plaintext = b""
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        # Decrypt block with key (XOR)
        decrypted = xor_bytes(block, key)
        # XOR decrypted block with prev ciphertext (or iv)
        xored = xor_blocks(decrypted, prev)
        plaintext += xored
        prev = block
    return plaintext

def main():
    key = bytes([1, 2, 3, 4, 5, 6, 7, 8])
    iv = bytes([0xAA, 0xBB, 0xCC, 0xDD, 0x11, 0x22, 0x33, 0x44])
    plaintext = b"CBCModeTestBlock1CBCModeTestBlock2"

    # Pad plaintext with zero bytes if needed
    if len(plaintext) % BLOCK_SIZE != 0:
        padding_len = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
        plaintext += b'\x00' * padding_len

    print("Plaintext:", plaintext.decode('utf-8', 'ignore'))

    ciphertext = cbc_encrypt(plaintext, key, iv)
    print("Ciphertext (hex):", ciphertext.hex())

    decrypted = cbc_decrypt(ciphertext, key, iv)
    decrypted = decrypted.rstrip(b'\x00')  # Remove padding zeros
    print("Decrypted Text:", decrypted.decode('utf-8', 'ignore'))

if __name__ == "__main__":
    main()
