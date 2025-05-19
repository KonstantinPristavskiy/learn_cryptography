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


def is_text_english(text: str) -> bool:
    english_words_list = get_english_words(ENGLISH_WORDS_PATH)
    english_words_amount = count_english_words(text, english_words_list)
    return True if english_words_amount / len(text.split(' ')) >= 0.8 else False
    
    

if __name__ == "__main__":
    
    text = "My name is mister black"
    is_text_english_result = is_text_english(text)
    print(is_text_english_result)
