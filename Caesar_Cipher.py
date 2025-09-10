def caesar_cipher(text, k):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) - ord('A') + k) % 26 + ord('A'))
        elif char.islower():
            result += chr((ord(char) - ord('a') + k) % 26 + ord('a'))
        else:
            result += char
    return result

# Example usage: Encrypt "HelloWorld" with shifts from 1 to 25
message = "we are in collage"
for k in range(1, 26):
    encrypted = caesar_cipher(message, k)
    print(f"Shift {k}: {encrypted}")
