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


if __name__ == "__main__":
        
    m = """Learning a little each day adds up Research shows that students who make learning a habit are more likely to reach their goals Set time aside to learn and get reminders using your learning scheduler"""
    encrypted = caesar_encrypt(m)
    print(encrypted)
    decrypted = caesar_decrypt(encrypted)

    print(decrypted)