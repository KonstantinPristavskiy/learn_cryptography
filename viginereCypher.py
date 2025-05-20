ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" # 27 characters

def viginere_encrypt(plain_text: str, key: str) -> str:
    #make the text case insensitive
    plain_text = plain_text.upper()
    key = key.upper()
    cipher_text = ""
    key_index = 0
    for char in plain_text:
        # number of shifts = index of a character in an plain_text + index of a character in a key
        index = (ALPHABET.find(char) + ALPHABET.find(key[key_index])) % len(ALPHABET)
        cipher_text += ALPHABET[index]
        # increasing a key index. if we are at the end of the key, start with 0
        key_index = (key_index + 1) % len(key)
    return cipher_text


def viginere_decrypt(cipher_text: str, key: str) -> str:
    #make the text case insensitive
    cipher_text = cipher_text.upper()
    key = key.upper()
    plain_text = ""
    key_index = 0
    for char in cipher_text:
        # number of shifts = index of a character in an plain_text - index of a character in a key
        index = (ALPHABET.find(char) - ALPHABET.find(key[key_index])) % len(ALPHABET)
        plain_text += ALPHABET[index]
        # increasing a key index. if we are at the end of the key, start with 0
        key_index = (key_index + 1) % len(key)
    return plain_text   


if __name__ == "__main__":
    text = "I love to study cryptography as I want to become crypto and AI engineer"
    key = "Pomodoro"
    cipher_text = viginere_encrypt(text, key)
    plain_text = viginere_decrypt(cipher_text, key)
    print(plain_text)