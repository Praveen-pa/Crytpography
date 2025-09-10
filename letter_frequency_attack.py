import string

# English letter frequency percentages
english_freq = [
    8.167,  # A
    1.492,  # B
    2.782,  # C
    4.253,  # D
    12.702, # E
    2.228,  # F
    2.015,  # G
    6.094,  # H
    6.966,  # I
    0.153,  # J
    0.772,  # K
    4.025,  # L
    2.406,  # M
    6.749,  # N
    7.507,  # O
    1.929,  # P
    0.095,  # Q
    5.987,  # R
    6.327,  # S
    9.056,  # T
    2.758,  # U
    0.978,  # V
    2.360,  # W
    0.150,  # X
    1.974,  # Y
    0.074   # Z
]

def caesar_decrypt(text, key):
    decrypted = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shifted = (ord(ch) - base - key + 26) % 26 + base
            decrypted.append(chr(shifted))
        else:
            decrypted.append(ch)
    return ''.join(decrypted)

def compute_score(text):
    # Compute score based on letter frequency similarity
    counts = [0]*26
    total = 0
    for ch in text:
        if ch.isalpha():
            counts[ord(ch.lower()) - ord('a')] += 1
            total += 1
    if total == 0:
        return 0
    score = 0
    for i in range(26):
        observed = counts[i] * 100.0 / total
        score += english_freq[i] * observed
    return score

def letter_frequency_attack(ciphertext, top_n):
    results = []
    for key in range(26):
        plaintext = caesar_decrypt(ciphertext, key)
        score = compute_score(plaintext)
        results.append((key, score, plaintext))
    # Sort descending by score
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]

def main():
    ciphertext = input("Enter ciphertext (Caesar-encrypted):\n").strip()
    top_n = int(input("Enter number of top possible plaintexts to display (e.g. 5 or 10):\n"))
    top_results = letter_frequency_attack(ciphertext, top_n)
    print(f"\nTop {top_n} most likely plaintexts:")
    for key, score, plaintext in top_results:
        print(f"\n[Key = {key:2d}] Score = {score:.2f}\n{plaintext}")

if __name__ == "__main__":
    main()
