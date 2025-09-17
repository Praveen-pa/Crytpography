import random
import string
import re
from collections import Counter
import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH_FREQ_ORDER = "ETAOINSHRDLUCMWFGYPBVKJXQZ"
COMMON_WORDS = ["the","and","that","have","for","not","with","you","this","but","his","from","they","say","her","she","will","one","all","would","there","their","what","so","up","out","if","about"]

# ----------------- Utilities -----------------
def clean_text(txt):
    return "".join(c for c in txt.upper() if c.isalpha() or c.isspace())

def count_common_words(text):
    text_lower = text.lower()
    return sum(len(re.findall(r'\b' + re.escape(word) + r'\b', text_lower)) for word in COMMON_WORDS)

def score_plaintext(text):
    s = re.sub(r'[^A-Z]', '', text.upper())
    word_score = count_common_words(text) * 10
    letter_score = sum([abs((s.count(c)/len(s)*100) - freq) for c,freq in zip(ALPHABET,[8.2,1.5,2.8,4.3,12,2.2,2.0,6.1,7.0,0.15,0.77,4.0,2.4,6.7,7.5,1.9,0.095,6.0,6.3,9.1,2.8,1.0,2.4,0.15,2.0,0.074])])
    return word_score - letter_score*0.1

def text_with_key(ciphertext, key):
    mapping = {ALPHABET[i]: key[i] for i in range(26)}
    result = []
    for ch in ciphertext.upper():
        if ch in ALPHABET:
            result.append(mapping[ch])
        else:
            result.append(ch)
    return "".join(result)

# ----------------- Key Helpers -----------------
def initial_key_by_frequency(ciphertext):
    s = re.sub(r'[^A-Z]', '', ciphertext.upper())
    freq_order = [c for c,_ in Counter(s).most_common()]
    key_mapping = {}
    for i, c in enumerate(freq_order):
        if i < len(ENGLISH_FREQ_ORDER):
            key_mapping[c] = ENGLISH_FREQ_ORDER[i]
    key = []
    used_letters = set(key_mapping.values())
    unused_letters = [c for c in ALPHABET if c not in used_letters]
    for c in ALPHABET:
        key.append(key_mapping.get(c, unused_letters.pop(0)))
    return "".join(key)

def random_neighbor_key(key):
    lst = list(key)
    i,j = random.sample(range(26),2)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)

# ----------------- Hill Climbing -----------------
def improve_key(ciphertext, key, iterations=2000):
    best_key = key
    best_text = text_with_key(ciphertext, best_key)
    best_score = score_plaintext(best_text)
    current_key = best_key
    current_score = best_score
    for i in range(iterations):
        neighbor = random_neighbor_key(current_key)
        neighbor_text = text_with_key(ciphertext, neighbor)
        neighbor_score = score_plaintext(neighbor_text)
        if neighbor_score > current_score or random.random() < 0.01:
            current_key = neighbor
            current_score = neighbor_score
            if current_score > best_score:
                best_key = current_key
                best_score = current_score
    return best_key, best_score

# ----------------- Solver -----------------
def solve_substitution(ciphertext, top_k=10, restarts=10):
    candidates = []
    freq_key = initial_key_by_frequency(ciphertext)
    k, s = improve_key(ciphertext, freq_key)
    candidates.append((s, text_with_key(ciphertext,k), k))
    for _ in range(restarts-1):
        rand_key = ''.join(random.sample(ALPHABET,26))
        k, s = improve_key(ciphertext, rand_key)
        candidates.append((s, text_with_key(ciphertext,k), k))
    # Sort by score descending
    unique = {}
    for score, text, key in candidates:
        if text not in unique or score > unique[text][0]:
            unique[text] = (score,key)
    results = sorted([(s,t,k) for t,(s,k) in unique.items()], key=lambda x:-x[0])
    return results[:top_k]

# ----------------- CLI -----------------
def main():
    print("Monoalphabetic Substitution Cipher Solver")
    ciphertext = input("Enter ciphertext: ").strip()
    top_k = input("Number of top candidates to show (default 10): ").strip()
    top_k = int(top_k) if top_k.isdigit() else 10
    print("Solving, please wait...")
    results = solve_substitution(ciphertext, top_k=top_k)
    for rank,(score, text, key) in enumerate(results,1):
        print(f"\nCandidate #{rank} (score={score:.2f})")
        print("Key (cipher->plain):")
        print(' '.join(f"{ALPHABET[i]}->{key[i]}" for i in range(26)))
        print("Plaintext:")
        print(text)

if __name__=="__main__":
    main()
