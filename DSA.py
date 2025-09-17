#!/usr/bin/env python3
"""
DSA demo: sign the same message twice and show signatures differ because of per-signature nonce k.
Requires: pip install cryptography
"""

from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
import binascii

def hexify(b: bytes) -> str:
    return binascii.hexlify(b).decode()

def main():
    # Generate a DSA private key (2048-bit)
    private_key = dsa.generate_private_key(key_size=2048)

    message = b"Test message for DSA signing"

    # Sign the message twice; DSA uses a random per-signature 'k', so signatures should differ.
    sig1 = private_key.sign(message, hashes.SHA256())
    sig2 = private_key.sign(message, hashes.SHA256())

    print("Message:", message)
    print("Signature 1 (hex):", hexify(sig1))
    print("Signature 2 (hex):", hexify(sig2))
    print("Signatures equal?:", sig1 == sig2)

if __name__ == "__main__":
    main()
