import matplotlib.pylab as plt
import ceasar
ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" # 27 characters

# SPACE is the most frequent symbol in a string, so we need to delete it from letters
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"





# in this analysis we need to count occurences of given characters
def frequency_analysis(text):
    # text we analyse
    text = text.upper()
    # using a dictionary for letter-frequency pair
    letter_frequences = {}
    # initialise the dictionary with 0 frequencies
    for letter in LETTERS:
        letter_frequences[letter] = 0

    # count the letter in the text
    for letter in text:
        if letter in LETTERS:
            letter_frequences[letter] += 1
    
    return letter_frequences

# making a hystogram
def plot_distribution(frequencies):
    plt.bar(frequencies.keys(), frequencies.values())
    plt.show()

def caesar_crack(cipher_text):
    freq = frequency_analysis(cipher_text)
    freq = sorted(freq.items(), key = lambda x: x[1], reverse=True)
    # print(freq)
    possible_key = LETTERS.find(freq[0][0])-LETTERS.find('E')
    print(f"The possible key value: {possible_key}")

if __name__ == "__main__":

    plain_text = "LearningalittleeachdayaddsupResearchshowsthatstudentswhomakelearningahabitaremorelikelytoreachtheirgoalsSettimeasidetolearnandgetremindersusingyourlearningscheduler"

    cipher_text = ceasar.caesar_encrypt(plain_text)
    print(cipher_text)
    caesar_crack(cipher_text)
