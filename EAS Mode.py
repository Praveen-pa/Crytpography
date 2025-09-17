from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# -------- Padding Function (1 followed by 0s) --------
def pad_message(message: bytes, block_size: int) -> bytes:
    """
    Pads the message using 1 followed by 0s until block_size.
    Always adds padding, even if already aligned.
    """
    padding_len = block_size - (len(message) % block_size)
    if padding_len == 0:
        padding_len = block_size
    # first bit = 1, rest = 0s
    padding = b'\x80' + b'\x00' * (padding_len - 1)
    return message + padding

# -------- ECB Encryption / Decryption --------
def ecb_encrypt(plaintext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad_message(plaintext, AES.block_size)
    return cipher.encrypt(padded)

def ecb_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted  # (includes padding for demo)

# -------- CBC Encryption / Decryption --------
def cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad_message(plaintext, AES.block_size)
    return cipher.encrypt(padded)

def cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted  # (includes padding for demo)

# -------- CFB Encryption / Decryption --------
def cfb_encrypt(plaintext: bytes, key: bytes, iv: bytes, segment_size: int = 128) -> bytes:
    cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=segment_size)
    padded = pad_message(plaintext, AES.block_size)  # pad for demonstration
    return cipher.encrypt(padded)

def cfb_decrypt(ciphertext: bytes, key: bytes, iv: bytes, segment_size: int = 128) -> bytes:
    cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=segment_size)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

# -------- Main Test --------
if __name__ == "__main__":
    key = get_random_bytes(16)  # AES-128 key
    iv = get_random_bytes(16)   # IV for CBC/CFB
    plaintext = b"Hello AES Modes Example"

    print("Original Plaintext:", plaintext)

    # ECB
    ecb_ct = ecb_encrypt(plaintext, key)
    ecb_pt = ecb_decrypt(ecb_ct, key)
    print("\nECB Mode:")
    print("Ciphertext:", ecb_ct.hex())
    print("Decrypted:", ecb_pt)

    # CBC
    cbc_ct = cbc_encrypt(plaintext, key, iv)
    cbc_pt = cbc_decrypt(cbc_ct, key, iv)
    print("\nCBC Mode:")
    print("Ciphertext:", cbc_ct.hex())
    print("Decrypted:", cbc_pt)

    # CFB
    cfb_ct = cfb_encrypt(plaintext, key, iv)
    cfb_pt = cfb_decrypt(cfb_ct, key, iv)
    print("\nCFB Mode:")
    print("Ciphertext:", cfb_ct.hex())
    print("Decrypted:", cfb_pt)
