ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" # 27 characters

KEY = 3



def caesar_encrypt(plain_text):
    cipher_text = ''
    plain_text = plain_text.upper()
    for c in plain_text:
        index = ALPHABET.find(c)
        index = (index + KEY) % len(ALPHABET)
        cipher_text = cipher_text + ALPHABET[index]

    return(cipher_text)



def caesar_decrypt(cipher_text):
    plain_text = ''
    cipher_text = cipher_text.upper()
    for c in cipher_text:
        index = ALPHABET.find(c)
        index = (index - KEY) % len(ALPHABET)
        plain_text = plain_text + ALPHABET[index]

    return(plain_text)



m = "Welcome to my Udemy course"
encrypted = caesar_encrypt(m)

decrypted = caesar_decrypt(encrypted)

print(decrypted)