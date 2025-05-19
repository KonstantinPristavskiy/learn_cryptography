from language_detector import *
ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" # 27 characters

# SPACE is the most frequent symbol in a string, so we need to delete it from letters
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def crack_brute_force_with_english_detection(cipher_text: str):
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
        is_text_english_result = is_text_english(plain_text)
        if is_text_english_result:
            return f"The decryption was succesfull, key: {key}, plain text: {plain_text}"
    return "Text could not be cracked"



if __name__ == "__main__":
    encrypted = "OHDUQLQJCDCOLWWOHCHDFKCGDACDGGVCXSCUHVHDUFKCVKRZVCWKDWCVWXGHQWVCZKRCPDNHCOHDUQLQJCDCKDELWCDUHCPRUHCOLNHOACWRCUHDFKCWKHLUCJRDOVCVHWCWLPHCDVLGHCWRCOHDUQCDQGCJHWCUHPLQGHUVCXVLQJCARXUCOHDUQLQJCVFKHGXOHU"


    print(crack_brute_force_with_english_detection(encrypted))

