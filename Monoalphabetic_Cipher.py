def generate_cipher_alphabet(keyword):
    used = set()
    cipher = []

    # Add unique letters from the keyword
    for ch in keyword.upper():
        if 'A' <= ch <= 'Z' and ch not in used:
            cipher.append(ch)
            used.add(ch)
    
    # Add remaining letters of the alphabet
    for ch in (chr(i) for i in range(ord('A'), ord('Z') + 1)):
        if ch not in used:
            cipher.append(ch)

    return cipher

def encrypt(plaintext, cipher):
    ciphertext = []
    for ch in plaintext:
        if ch.isalpha():
            index = ord(ch.lower()) - ord('a')
            ciphertext.append(cipher[index])
        else:
            ciphertext.append(ch)
    return ''.join(ciphertext)

def main():
    keyword = input("Enter keyword: ")
    cipher = generate_cipher_alphabet(keyword)

    print("Generated Cipher Alphabet:")
    print("Plain : " + ' '.join(chr(i) for i in range(ord('A'), ord('Z') + 1)))
    print("Cipher: " + ' '.join(cipher))
    print()

    plaintext = input("Enter plaintext: ")
    ciphertext = encrypt(plaintext, cipher)

    print("Encrypted text:", ciphertext)

if __name__ == "__main__":
    main()
