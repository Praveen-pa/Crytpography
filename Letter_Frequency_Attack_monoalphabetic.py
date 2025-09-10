import string

english_freq_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def compute_score(text):
    score = 0
    for ch in text:
        c = ch.lower()
        if c == ' ':
            score += 2
        if c in "etaoinshrdlu":
            score += 1
    return score

def decrypt_with_key(ciphertext, mapping):
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            idx = ord(ch.upper()) - ord('A')
            mapped_char = mapping[idx]
            if ch.isupper():
                result.append(mapped_char.upper())
            else:
                result.append(mapped_char.lower())
        else:
            result.append(ch)
    return ''.join(result)

def frequency_analysis(ciphertext):
    freq = {ch:0 for ch in string.ascii_uppercase}
    for ch in ciphertext:
        if ch.isalpha():
            freq[ch.upper()] += 1
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [ch for ch, count in sorted_freq]

def letter_frequency_attack(ciphertext, top_n):
    freq_ordered_letters = frequency_analysis(ciphertext)
    results = []
    max_tries = 26
    alphabet = string.ascii_uppercase
    for shift in range(max_tries):
        key_map = [''] * 26
        for i, ch in enumerate(freq_ordered_letters):
            key_map[ord(ch) - ord('A')] = english_freq_order[(i + shift) % 26]
        plaintext = decrypt_with_key(ciphertext, key_map)
        score = compute_score(plaintext)
        results.append((plaintext, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]

def main():
    ciphertext = input("Enter monoalphabetic ciphertext:\n").strip()
    top_n = int(input("Enter number of top guesses to display:\n"))
    top_results = letter_frequency_attack(ciphertext, top_n)
    print(f"\nTop {top_n} possible plaintexts:")
    for i, (plaintext, score) in enumerate(top_results, 1):
        print(f"\n[{i}] Score: {score:.2f}\n{plaintext}")

if __name__ == "__main__":
    main()
