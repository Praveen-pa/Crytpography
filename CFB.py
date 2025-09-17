from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# --- Padding function: 1 followed by 0's ---
def custom_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:   # always add an extra block of padding
        pad_len = block_size
    return data + b'\x80' + b'\x00' * (pad_len - 1)

# --- Unpadding function ---
def custom_unpad(data: bytes) -> bytes:
    return data.rstrip(b'\x00').rstrip(b'\x80')

# --- Encrypt / Decrypt ECB ---
def ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded = custom_pad(plaintext, AES.block_size)
    return cipher.encrypt(padded)

def ecb_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return custom_unpad(decrypted)

# --- Encrypt / Decrypt CBC ---
def cbc_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = custom_pad(plaintext, AES.block_size)
    return cipher.encrypt(padded)

def cbc_decrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return custom_unpad(decrypted)

# --- Encrypt / Decrypt CFB ---
def cfb_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    return cipher.encrypt(plaintext)  # no padding needed in CFB

def cfb_decrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    return cipher.decrypt(ciphertext)


# ---------------------- TEST ----------------------
if __name__ == "__main__":
    key = get_random_bytes(16)  # AES-128 key
    iv = get_random_bytes(16)
    plaintext = b"HELLO BLOCK CIPHERS"

    # ECB
    ecb_ct = ecb_encrypt(key, plaintext)
    print("ECB decrypted:", ecb_decrypt(key, ecb_ct))

    # CBC
    cbc_ct = cbc_encrypt(key, plaintext, iv)
    print("CBC decrypted:", cbc_decrypt(key, cbc_ct, iv))

    # CFB
    cfb_ct = cfb_encrypt(key, plaintext, iv)
    print("CFB decrypted:", cfb_decrypt(key, cfb_ct, iv))
