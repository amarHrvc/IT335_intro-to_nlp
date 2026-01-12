"""
NLP MIDTERM EXAM - SOLUTION TEMPLATE
=====================================
Copy this file and modify as needed for your exam.

Tasks covered:
- Task 1: Text processing (read, clean, tokenize, FreqDist, CFD, emails)
- Task 2: Gutenberg corpus + WordNet
- Task 3: Brown corpus + Bigram tagger
"""

# ============================================================
# SETUP - Run this section first
# ============================================================
import nltk
import re
import string
import matplotlib.pyplot as plt

# Download required data (run once, then comment out)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('universal_tagset')
nltk.download('brown')
nltk.download('gutenberg')
nltk.download('wordnet')

from nltk import word_tokenize, FreqDist, ConditionalFreqDist
from nltk.corpus import gutenberg, brown, wordnet
from nltk import DefaultTagger, UnigramTagger, BigramTagger


# ============================================================
# TASK 1: TEXT PROCESSING
# ============================================================

def task1_text_processing(filename):
    """
    Process a text file:
    1. (2pts) Read the file
    2. (6pts) Clean: remove punctuation, lowercase, extract emails
    3. (5pts) Tokenize
    4. (5pts) Count frequency, show top 10
    5. (10pts) CFD: word length by starting letter (a, b, c)
    6. (2pts) Return extracted emails
    """

    # --- Task 1.1: Read file (2pts) ---
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    print("=== Task 1.1: File Content (first 200 chars) ===")
    print(text[:200])
    print()

    # --- Task 1.2: Clean text (6pts) ---
    # Extract emails FIRST (before removing punctuation)
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)

    # Remove punctuation
    text_clean = text.translate(str.maketrans('', '', string.punctuation))

    # Convert to lowercase
    text_lower = text_clean.lower()

    print("=== Task 1.2: Cleaned Text (first 200 chars) ===")
    print(text_lower[:200])
    print()

    # --- Task 1.3: Tokenize (5pts) ---
    tokens = word_tokenize(text_lower)
    # Keep only alphabetic words
    words = [token for token in tokens if token.isalpha()]

    print("=== Task 1.3: Tokenization ===")
    print(f"Total tokens: {len(tokens)}")
    print(f"Alphabetic words: {len(words)}")
    print(f"First 10 words: {words[:10]}")
    print()

    # --- Task 1.4: Frequency Distribution - Top 10 (5pts) ---
    fdist = FreqDist(words)
    top_10 = fdist.most_common(10)

    print("=== Task 1.4: Top 10 Most Frequent Words ===")
    for word, count in top_10:
        print(f"  {word}: {count}")
    print()

    # --- Task 1.5: Conditional Frequency Distribution (10pts) ---
    # Word length distribution for words starting with a, b, c
    target_letters = ['a', 'b', 'c']

    cfd = ConditionalFreqDist(
        (word[0], len(word))  # (first_letter, word_length)
        for word in words
        if len(word) > 0 and word[0] in target_letters
    )

    print("=== Task 1.5: Word Length by Starting Letter ===")
    for letter in target_letters:
        print(f"  Words starting with '{letter}':")
        for length, count in sorted(cfd[letter].items()):
            print(f"    Length {length}: {count} words")
    print()

    # Plot CFD
    cfd.plot()
    plt.title("Word Length Distribution by Starting Letter")
    plt.xlabel("Word Length")
    plt.ylabel("Frequency")
    plt.show()

    # --- Task 1.6: Return emails (2pts) ---
    print("=== Task 1.6: Extracted Emails ===")
    print(f"  {emails}")
    print()

    return {
        'text': text_lower,
        'words': words,
        'top_10': top_10,
        'cfd': cfd,
        'emails': emails
    }


# ============================================================
# TASK 2: GUTENBERG + WORDNET
# ============================================================

def task2_gutenberg_wordnet():
    """
    1. (10pts) Find most common word in Gutenberg corpus
    2. (10pts) Find synonyms and antonyms using WordNet
    """

    # --- Task 2.1: Most common word in Gutenberg (10pts) ---
    print("=== Task 2.1: Most Common Word in Gutenberg ===")

    # Get all words from Gutenberg
    all_words = gutenberg.words()

    # Clean: lowercase and alphabetic only
    words = [w.lower() for w in all_words if w.isalpha()]

    # Frequency distribution
    fdist = FreqDist(words)

    # Most common word
    most_common_word, frequency = fdist.most_common(1)[0]

    print(f"  Most common word: '{most_common_word}'")
    print(f"  Frequency: {frequency}")
    print()

    # --- Task 2.2: Synonyms and Antonyms (10pts) ---
    print(f"=== Task 2.2: Synonyms/Antonyms for '{most_common_word}' ===")

    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(most_common_word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            for ant in lemma.antonyms():
                antonyms.append(ant.name())

    # Remove duplicates
    synonyms = list(set(synonyms))
    antonyms = list(set(antonyms))

    print(f"  Synonyms: {synonyms}")
    print(f"  Antonyms: {antonyms}")
    print()

    return {
        'most_common_word': most_common_word,
        'frequency': frequency,
        'synonyms': synonyms,
        'antonyms': antonyms
    }


# ============================================================
# TASK 3: BROWN CORPUS + BIGRAM TAGGER
# ============================================================

def task3_pos_tagging():
    """
    1. (10pts) Train Bigram tagger on Brown corpus (universal_tagset)
    2. (10pts) Tag: "The quick brown fox jumps over the lazy dog."
    3. (5pts) Return tagged sentence and accuracy
    """

    # --- Task 3.1: Train Bigram Tagger (10pts) ---
    print("=== Task 3.1: Training Bigram Tagger ===")

    # Get tagged sentences with universal tagset
    tagged_sents = brown.tagged_sents(tagset='universal')

    # Split: 90% train, 10% test
    train_size = int(len(tagged_sents) * 0.9)
    train_sents = tagged_sents[:train_size]
    test_sents = tagged_sents[train_size:]

    print(f"  Training sentences: {len(train_sents)}")
    print(f"  Test sentences: {len(test_sents)}")

    # Build tagger chain with backoff
    t0 = DefaultTagger('NOUN')  # Default: guess NOUN
    t1 = UnigramTagger(train_sents, backoff=t0)
    t2 = BigramTagger(train_sents, backoff=t1)

    print("  Bigram tagger trained successfully!")
    print()

    # --- Task 3.2: Tag the sentence (10pts) ---
    print("=== Task 3.2: Tagging Sentence ===")

    sentence = "The quick brown fox jumps over the lazy dog."
    tokens = word_tokenize(sentence)
    tagged_sentence = t2.tag(tokens)

    print(f"  Original: {sentence}")
    print(f"  Tagged: {tagged_sentence}")
    print()

    # --- Task 3.3: Calculate Accuracy (5pts) ---
    print("=== Task 3.3: Tagger Accuracy ===")

    accuracy = t2.accuracy(test_sents)
    print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print()

    return {
        'tagged_sentence': tagged_sentence,
        'accuracy': accuracy
    }


# ============================================================
# MAIN - Run all tasks
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NLP MIDTERM EXAM - RUNNING ALL TASKS")
    print("=" * 60)
    print()

    # Task 1: Uncomment and provide your file path
    # result1 = task1_text_processing('task1.txt')

    # Task 2
    result2 = task2_gutenberg_wordnet()

    # Task 3
    result3 = task3_pos_tagging()

    print("=" * 60)
    print("ALL TASKS COMPLETED")
    print("=" * 60)
