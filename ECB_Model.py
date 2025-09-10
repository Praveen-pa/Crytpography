BLOCK_SIZE = 8

def xor_encrypt_block(block, key):
    return bytes([b ^ k for b, k in zip(block, key)])

def ecb_encrypt(plaintext, key):
    ciphertext = b''
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        ciphertext += xor_encrypt_block(block, key)
    return ciphertext

def ecb_decrypt(ciphertext, key):
    plaintext = b''
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        plaintext += xor_encrypt_block(block, key)
    return plaintext

def main():
    key = bytes([1, 2, 3, 4, 5, 6, 7, 8])
    plaintext = b"ThisIsBlock1ThisIsBlock2"  # 22 bytes, 2 full blocks and partial last

    # Pad plaintext to multiple of BLOCK_SIZE with zeros
    padding_len = (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) % BLOCK_SIZE
    plaintext_padded = plaintext + b'\x00' * padding_len

    print("Original Plaintext:", plaintext.decode('utf-8'))

    ciphertext = ecb_encrypt(plaintext_padded, key)
    print("Ciphertext (hex):", ciphertext.hex())

    decrypted = ecb_decrypt(ciphertext, key)
    decrypted = decrypted.rstrip(b'\x00')  # Remove padding zeros
    print("Decrypted Plaintext:", decrypted.decode('utf-8'))

    # Introduce an error in ciphertext block 1 (simulate bit flip in block 1)
    error_position = BLOCK_SIZE  # Start of second block
    corrupted_ciphertext = bytearray(ciphertext)
    corrupted_ciphertext[error_position] ^= 0x01  # Flip least significant bit of first byte of block 2

    print("\nAfter error introduced in ciphertext block 2:")
    decrypted_corrupted = ecb_decrypt(bytes(corrupted_ciphertext), key)
    decrypted_corrupted = decrypted_corrupted.rstrip(b'\x00')
    print("Decrypted Plaintext with error:", decrypted_corrupted.decode('utf-8', 'replace'))

if __name__ == "__main__":
    main()
