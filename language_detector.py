ENGLISH_WORDS_PATH = 'english_words.txt'

def get_english_words(path: str) -> list:
    with open(path, 'r') as file:
        english_words = [line.strip() for line in file.readlines()]
        return english_words

def count_english_words(text: str, english_words_list: list) -> int:
    text = text.upper()
    words = text.split(' ')
    matches = sum(1 for word in words if word in english_words_list)
    return matches


if __name__ == "__main__":
    english_words_list = get_english_words(ENGLISH_WORDS_PATH)
    print(len(english_words_list))

    text = "My name is Kostiantyn"
    english_words_amount = count_english_words(text, english_words_list)
    print(english_words_amount)
    