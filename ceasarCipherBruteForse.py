ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" # 27 characters

KEY = 1

def crack_caesar(cipher_text):
    # try all the possible KEY values
    for key in range(len(ALPHABET)):
        # reinitialize this to be an empty string
        plain_text = ''

        # make a simple decryption
        for c in cipher_text:
            index = ALPHABET.find(c)
            index = (index-key) % len(ALPHABET)
            plain_text = plain_text + ALPHABET[index]
        #print the actual decrypted string with the given key
        print(f"With key {key}, the result is {plain_text}")


if __name__ == "__main__":
    encrypted = "ZHOFRPHCWRCPACXGHPACFRXUVH"


    crack_caesar(encrypted)



