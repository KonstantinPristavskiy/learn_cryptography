import math
import re
from collections import Counter
import ceasarCipherFrequencyAnalysis as caesar_analysis
import language_detector
import viginereCypher

ALPHABET = viginereCypher.ALPHABET
LETTERS = caesar_analysis.LETTERS

def preprocess_text(text):
    """Preprocess the text to keep only letters and spaces."""
    return re.sub(r'[^A-Z ]', '', text.upper())

def find_repeated_sequences(text, seq_length=3):
    """
    Find all repeated sequences of specified length in the text
    and their positions.
    """
    sequences = {}
    for i in range(len(text) - seq_length + 1):
        seq = text[i:i+seq_length]
        # Only consider sequences with at least 2 letters (no spaces only)
        if sum(1 for c in seq if c in LETTERS) >= 2:
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
    
    # Filter out sequences that don't repeat
    return {seq: positions for seq, positions in sequences.items() if len(positions) > 1}

def calculate_spacings(positions):
    """Calculate the distance between consecutive positions."""
    return [positions[i+1] - positions[i] for i in range(len(positions) - 1)]

def find_key_length(repeated_sequences):
    """
    Calculate potential key lengths by finding the GCD of the spacings
    between repeated sequences.
    """
    all_spacings = []
    for positions in repeated_sequences.values():
        spacings = calculate_spacings(positions)
        all_spacings.extend(spacings)
    
    # Count occurrences of each spacing
    spacing_counts = Counter(all_spacings)
    
    # Calculate GCDs of all spacing combinations
    gcds = []
    for spacing1 in spacing_counts:
        for spacing2 in spacing_counts:
            if spacing1 < spacing2:  # Avoid duplicate calculations
                gcd = math.gcd(spacing1, spacing2)
                if gcd > 1:  # Ignore GCD of 1 as it's not helpful
                    gcds.append(gcd)
    
    # Count occurrences of each GCD
    gcd_counts = Counter(gcds)
    
    # Return the most common GCDs as potential key lengths
    most_common = gcd_counts.most_common(5)
    return [length for length, _ in most_common] if most_common else list(range(3, 8))  # Try common lengths if no GCDs found

def split_into_columns(text, key_length):
    """Split the ciphertext into columns based on key length."""
    columns = [''] * key_length
    for i, char in enumerate(text):
        if char in LETTERS:  # Only process letters
            columns[i % key_length] += char
    return columns

def get_letter_frequencies(text):
    """Get letter frequencies for the given text."""
    freq = {}
    for letter in LETTERS:
        freq[letter] = 0
    
    for char in text:
        if char in LETTERS:
            freq[char] += 1
    
    total = sum(freq.values())
    if total > 0:
        for letter in freq:
            freq[letter] /= total
    
    return freq

def determine_key(columns):
    """
    Determine the key by performing frequency analysis on each column,
    treating each column as a Caesar cipher.
    """
    key = ''
    most_common_english = 'E'  # Most common letter in English
    
    for column in columns:
        freq = caesar_analysis.frequency_analysis(column)
        # Find the most frequent letter in the column
        most_frequent = max(freq.items(), key=lambda x: x[1])[0]
        
        # Calculate the shift needed to convert most_frequent to most_common_english
        # For Vigenère, the key letter is what you add to plaintext to get ciphertext
        # So the key letter is the shift that transforms plaintext to ciphertext
        shift = get_shift(most_common_english, most_frequent)
        
        # Convert shift to letter
        key_char = ALPHABET[shift]
        key += key_char
    
    return key

def try_decrypt(cipher_text, key):
    """Try to decrypt the ciphertext with the given key and check if it's English."""
    try:
        decrypted = viginereCypher.viginere_decrypt(cipher_text, key)
        
        # Check if result is English
        english_words_list = language_detector.get_english_words(language_detector.ENGLISH_WORDS_PATH)
        english_word_count = language_detector.count_english_words(decrypted, english_words_list)
        
        # Calculate score based on proportion of English words
        words = decrypted.split()
        score = english_word_count / max(1, len(words)) if words else 0
        
        return decrypted, score
    except Exception as e:
        print(f"Error decrypting with key {key}: {e}")
        return "", 0

def brute_force_key(cipher_text, key_length):
    """
    Try to brute force the key by trying different letter combinations.
    For short keys (<=4), we can try all combinations.
    """
    if key_length > 7:
        return None, None, 0  # Too many combinations to try
    
    print(f"Brute forcing key of length {key_length}...")
    best_key = None
    best_plaintext = None
    best_score = 0
    
    # For a real implementation, we would use frequency analysis to narrow down
    # the possibilities for each position. For this demo, let's try a few common
    # English letters for each position to limit the search space.
    common_letters = 'ETAOINSHRDLUCMFWYP'
    
    # Try keys using common English letters
    # For very short keys, we can try all possible combinations
    if key_length <= 3:
        # Try all combinations for short keys
        letters_to_try = LETTERS
    else:
        # Try only common letters for longer keys
        letters_to_try = common_letters
    
    # For this demo, limit to testing the first few combinations
    max_combinations = 100  # Limit to prevent long execution time
    count = 0
    
    def generate_keys(prefix, depth):
        nonlocal count, best_key, best_plaintext, best_score
        
        if count >= max_combinations:
            return
        
        if depth == 0:
            count += 1
            # Try this key
            decrypted, score = try_decrypt(cipher_text, prefix)
            if score > best_score:
                best_score = score
                best_key = prefix
                best_plaintext = decrypted
                print(f"  New best key: {best_key} (score: {best_score:.2f})")
            return
        
        for letter in letters_to_try:
            generate_keys(prefix + letter, depth - 1)
    
    # Start generating keys
    generate_keys('', key_length)
    
    return best_key, best_plaintext, best_score

def try_known_key_patterns(cipher_text):
    """Try some common key patterns that might work."""
    common_keys = ["CRYPTO", "SECRET", "KEY", "CIPHER", "PASSWORD", "CODE", "VIGENERE"]
    
    best_key = None
    best_plaintext = None
    best_score = 0
    
    print("Trying known key patterns...")
    for key in common_keys:
        decrypted, score = try_decrypt(cipher_text, key)
        print(f"  Key '{key}': score {score:.2f}")
        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = decrypted
    
    return best_key, best_plaintext, best_score

def frequency_analysis_approach(cipher_text, key_length):
    """Use frequency analysis to determine the key."""
    columns = split_into_columns(cipher_text, key_length)
    
    # For each column, find the shift that produces the most English-like distribution
    key = ""
    for col in columns:
        best_shift = 0
        best_score = 0
        
        for shift in range(len(ALPHABET)):
            # Apply shift and analyze letter frequency
            shifted_col = ""
            for char in col:
                if char in ALPHABET:
                    idx = (ALPHABET.find(char) - shift) % len(ALPHABET)
                    shifted_col += ALPHABET[idx]
            
            # Score based on common letter frequencies in English
            score = 0
            freq = get_letter_frequencies(shifted_col)
            # E, T, A, O, I, N are the most common letters in English
            for letter, weight in [('E', 0.12), ('T', 0.09), ('A', 0.08), ('O', 0.07), ('I', 0.07), ('N', 0.07)]:
                score += freq[letter] * weight
            
            if score > best_score:
                best_score = score
                best_shift = shift
        
        # Convert shift to key character
        key += ALPHABET[best_shift]
    
    decrypted, score = try_decrypt(cipher_text, key)
    return key, decrypted, score

def kasiski_crack(cipher_text):
    """
    Crack a Vigenère cipher using multiple approaches:
    1. Try some common keys directly
    2. Use Kasiski examination to find key length
    3. Try frequency analysis for each potential key length
    4. Brute force for short key lengths
    """
    # Preprocess the cipher text
    cipher_text = preprocess_text(cipher_text)
    
    # Try some common keys first
    best_key, best_plaintext, best_score = try_known_key_patterns(cipher_text)
    
    # If we got a good match, return it
    if best_score > 0.5:
        return {
            'key': best_key,
            'plaintext': best_plaintext,
            'confidence': best_score,
            'method': 'known key pattern'
        }
    
    # Try to find key lengths with Kasiski examination
    repeated = find_repeated_sequences(cipher_text)
    potential_key_lengths = list(range(3, 8))  # Try key lengths 3-7
    
    if repeated:
        kasiski_lengths = find_key_length(repeated)
        print(f"Kasiski examination suggests key lengths: {kasiski_lengths}")
        # Add Kasiski lengths to the front of our list to prioritize them
        for length in reversed(kasiski_lengths):
            if length in potential_key_lengths:
                potential_key_lengths.remove(length)
            potential_key_lengths.insert(0, length)
    
    print(f"Trying key lengths: {potential_key_lengths}")
    
    # Try frequency analysis approach for each key length
    for length in potential_key_lengths:
        print(f"Trying frequency analysis for key length {length}...")
        key, plaintext, score = frequency_analysis_approach(cipher_text, length)
        print(f"  Key: {key}, Score: {score:.2f}")
        
        if score > best_score:
            best_key = key
            best_plaintext = plaintext
            best_score = score
            best_method = 'frequency analysis'
    
    # If we still don't have a good match, try brute force for short key lengths
    if best_score < 0.3:
        for length in [l for l in potential_key_lengths if l <= 5]:  # Only try brute force for short keys
            key, plaintext, score = brute_force_key(cipher_text, length)
            if score > best_score:
                best_key = key
                best_plaintext = plaintext
                best_score = score
                best_method = 'brute force'
    
    if best_key:
        return {
            'key': best_key,
            'plaintext': best_plaintext,
            'confidence': best_score,
            'method': best_method if best_score > 0 else 'none'
        }
    else:
        return {
            'key': None,
            'plaintext': None,
            'confidence': 0.0,
            'method': 'none'
        }

if __name__ == "__main__":
    # Example usage
    text = "I love to study cryptography as I want to become crypto and AI engineer"
    key = "CRYPTO"
    
    cipher_text = viginereCypher.viginere_encrypt(text, key)
    print(f"Original text: {text}")
    print(f"Cipher text: {cipher_text}")
    print(f"Original key: {key}")
    
    result = kasiski_crack(cipher_text)
    print(f"\nCracked result:")
    print(f"Detected key: {result['key']}")
    print(f"Decrypted text: {result['plaintext']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Method used: {result['method']}")
    
    # Test with a longer message
    print("\n--- Testing with a longer message ---")
    longer_text = ("The Vigenere cipher is a method of encrypting alphabetic text by using a simple "
                  "form of polyalphabetic substitution. A polyalphabetic cipher uses multiple "
                  "substitution alphabets to encrypt the plaintext. The Vigenere cipher is named "
                  "after Blaise de Vigenere although it was actually first described by Giovan "
                  "Battista Bellaso in his book from 1553.")
    longer_key = "SECURITYKEY"
    
    longer_cipher = viginereCypher.viginere_encrypt(longer_text, longer_key)
    print(f"Cipher text: {longer_cipher[:100]}...")
    
    longer_result = kasiski_crack(longer_cipher)
    print(f"\nCracked result:")
    print(f"Detected key: {longer_result['key']}")
    print(f"Decrypted text: {longer_result['plaintext'][:100]}...")
    print(f"Confidence: {longer_result['confidence']:.2f}")
    print(f"Method used: {longer_result['method']}") 