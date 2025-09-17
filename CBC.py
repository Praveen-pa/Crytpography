from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def pad_block(b: bytes, block_size=16) -> bytes:
    # Not needed for CBC-MAC on single-complete-block messages.
    if len(b) == block_size:
        return b
    raise ValueError("This demo expects exact single-block messages.")

def cbc_mac(key: bytes, message: bytes) -> bytes:
    """
    Simple CBC-MAC with zero IV. Expects message length to be a multiple of block size.
    Returns the tag (last ciphertext block).
    """
    block_size = AES.block_size
    if len(message) % block_size != 0:
        raise ValueError("Message must be a multiple of block size in this demo.")
    cipher = AES.new(key, AES.MODE_ECB)   # we'll do CBC manually (zero IV)
    iv = b'\x00' * block_size
    prev = iv
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]
        x = xor_bytes(block, prev)
        prev = cipher.encrypt(x)
    return prev  # last ciphertext block = MAC tag

if __name__ == "__main__":
    # Choose random AES key and a single-block message X
    key = get_random_bytes(16)
    X = b"EXACTLY_16_BYTES"   # 16 bytes exactly; you can use any 16-byte block
    assert len(X) == 16

    # Compute tag T for single-block message X
    T = cbc_mac(key, X)
    print("Single-block message X (hex):", X.hex())
    print("CBC-MAC tag T for X (hex):", T.hex())

    # Attacker constructs two-block message: X || (X XOR T)
    X_xor_T = xor_bytes(X, T)
    M_forge = X + X_xor_T
    print("\nForged two-block message M = X || (X XOR T):")
    print("Second block (X XOR T) (hex):", X_xor_T.hex())

    # Compute CBC-MAC of forged message
    T_forge = cbc_mac(key, M_forge)
    print("CBC-MAC tag T' for forged message (hex):", T_forge.hex())

    # Verify equality
    print("\nTag equals original?", T_forge == T)
