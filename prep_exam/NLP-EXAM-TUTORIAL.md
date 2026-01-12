# NLP with Python - Exam Prep Tutorial

**Goal:** Learn enough to score 60-70% on midterm + final in 2 days.
**Approach:** Copy-paste patterns with minimal explanation.

---

## Table of Contents

### DAY 1 - Midterm Topics
- [Module 1: Setup](#module-1-setup)
- [Module 2: Text Cleaning & Regex](#module-2-text-cleaning--regex)
  - [2.4 REGEX DEEP DIVE](#24-regex-deep-dive---how-to-build-patterns) (NEW - comprehensive patterns)
- [Module 3: Tokenization & Frequency](#module-3-tokenization--frequency)
- [Module 4: Corpora & WordNet](#module-4-corpora--wordnet)
- [Module 5: POS Tagging](#module-5-pos-tagging)

### DAY 2 - Final Topics
- [Module 6: Feature Extraction (BoW/TF-IDF)](#module-6-feature-extraction)
- [Module 7: Classification (Naive Bayes)](#module-7-classification)
- [Module 8: Chunking](#module-8-chunking)
- [Module 9: Cheat Sheet](#module-9-cheat-sheet)

---

# DAY 1 - MIDTERM TOPICS

---

## Module 1: Setup

### 1.1 Install Everything You Need

```python
# Run this ONCE before exam
pip install nltk scikit-learn matplotlib
```

### 1.2 All Imports You'll Ever Need

```python
# === COPY THIS TO TOP OF EVERY EXAM FILE ===
import nltk
import re
import string

# Download all required data (run once)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('universal_tagset')
nltk.download('brown')
nltk.download('gutenberg')
nltk.download('wordnet')
nltk.download('stopwords')

# Common imports
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk import FreqDist, ConditionalFreqDist
from nltk.corpus import gutenberg, brown, wordnet, stopwords
from nltk import RegexpParser

# For ML tasks (Final exam)
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
```

### 1.3 Read a File (Exam Task 1.1 - 2pts)

```python
# Pattern: Read entire file content
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# Usage
text = read_file('task1.txt')
print(text)
```

**What it does:** Opens file, reads all text, returns as string.

---

## Module 2: Text Cleaning & Regex

### 2.1 Remove Punctuation (Exam Task 1.2 - part of 6pts)

```python
import string

text = "Hello, World! How are you?"

# METHOD 1: Using translate (RECOMMENDED - fastest)
text_clean = text.translate(str.maketrans('', '', string.punctuation))
print(text_clean)  # "Hello World How are you"

# METHOD 2: Using replace in loop (slower but clear)
for char in string.punctuation:
    text = text.replace(char, '')
```

**What `string.punctuation` contains:** `!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`

### 2.2 Convert to Lowercase (Exam Task 1.2 - part of 6pts)

```python
text = "Hello World"
text_lower = text.lower()
print(text_lower)  # "hello world"
```

### 2.3 Extract Emails with Regex (Exam Task 1.2 & 1.6 - 2pts)

```python
import re

text = "Contact us at support@example.com or sales@company.org for help."

# Pattern to match emails
email_pattern = r'[\w\.-]+@[\w\.-]+'

# Find all emails
emails = re.findall(email_pattern, text)
print(emails)  # ['support@example.com', 'sales@company.org']
```

**Regex breakdown:**
- `[\w\.-]+` = one or more word chars, dots, or hyphens (before @)
- `@` = literal @ symbol
- `[\w\.-]+` = one or more word chars, dots, or hyphens (after @)

---

### 2.4 REGEX DEEP DIVE - How to Build Patterns

#### 2.4.1 The Basics - What is Regex?

Regex (Regular Expression) = a pattern that describes text you want to find.

```python
import re

text = "The cat sat on the mat"

# Find all words starting with 'c' or 'm'
matches = re.findall(r'\b[cm]\w+', text)
print(matches)  # ['cat', 'mat']
```

#### 2.4.2 Character Classes - WHAT to Match

| Pattern | Matches | Example | Finds in "Hello123" |
|---------|---------|---------|---------------------|
| `\w` | Word char (a-z, A-Z, 0-9, _) | `\w+` | `Hello123` |
| `\W` | NON-word char | `\W` | (nothing) |
| `\d` | Digit (0-9) | `\d+` | `123` |
| `\D` | NON-digit | `\D+` | `Hello` |
| `\s` | Whitespace (space, tab, newline) | `\s` | (spaces) |
| `\S` | NON-whitespace | `\S+` | `Hello123` |
| `.` | ANY character (except newline) | `.+` | `Hello123` |

```python
import re

text = "Order #12345 costs $99.99"

# Find all digits
digits = re.findall(r'\d+', text)
print(digits)  # ['12345', '99', '99']

# Find all non-digits (words, symbols)
non_digits = re.findall(r'\D+', text)
print(non_digits)  # ['Order #', ' costs $', '.']

# Find word characters
words = re.findall(r'\w+', text)
print(words)  # ['Order', '12345', 'costs', '99', '99']
```

#### 2.4.3 Quantifiers - HOW MANY to Match

| Pattern | Meaning | Example | Matches |
|---------|---------|---------|---------|
| `+` | One or more | `\d+` | "1", "123", "99999" |
| `*` | Zero or more | `\d*` | "", "1", "123" |
| `?` | Zero or one (optional) | `colou?r` | "color", "colour" |
| `{n}` | Exactly n | `\d{3}` | "123" (exactly 3 digits) |
| `{n,}` | n or more | `\d{2,}` | "12", "123", "1234" |
| `{n,m}` | Between n and m | `\d{2,4}` | "12", "123", "1234" |

```python
import re

# Phone number variations
texts = ["123-4567", "12-4567", "1234-4567"]

# Exactly 3 digits, dash, exactly 4 digits
pattern = r'\d{3}-\d{4}'
for t in texts:
    match = re.search(pattern, t)
    print(f"{t}: {match.group() if match else 'No match'}")
# 123-4567: 123-4567
# 12-4567: No match
# 1234-4567: 4-4567  (finds last 3-4 pattern)
```

#### 2.4.4 Character Sets - WHICH Characters

| Pattern | Meaning | Example |
|---------|---------|---------|
| `[abc]` | Any of a, b, or c | `[aeiou]` matches vowels |
| `[a-z]` | Any lowercase letter | `[a-z]+` matches words |
| `[A-Z]` | Any uppercase letter | `[A-Z]+` matches CAPS |
| `[0-9]` | Any digit (same as `\d`) | `[0-9]+` matches numbers |
| `[a-zA-Z]` | Any letter | `[a-zA-Z]+` matches words |
| `[^abc]` | NOT a, b, or c | `[^0-9]+` matches non-digits |

```python
import re

text = "Hello World 123"

# Only lowercase
lower = re.findall(r'[a-z]+', text)
print(lower)  # ['ello', 'orld']

# Only uppercase
upper = re.findall(r'[A-Z]+', text)
print(upper)  # ['H', 'W']

# Any letter (upper or lower)
letters = re.findall(r'[a-zA-Z]+', text)
print(letters)  # ['Hello', 'World']

# Not letters (digits and spaces)
not_letters = re.findall(r'[^a-zA-Z]+', text)
print(not_letters)  # [' ', ' ', '123']
```

#### 2.4.5 Anchors - WHERE to Match

| Pattern | Meaning | Example |
|---------|---------|---------|
| `^` | Start of string | `^Hello` matches "Hello world" |
| `$` | End of string | `world$` matches "Hello world" |
| `\b` | Word boundary | `\bcat\b` matches "cat" not "catalog" |
| `\B` | NOT word boundary | `\Bcat` matches "catalog" not "cat" |

```python
import re

text = "cat catalog catfish"

# 'cat' as whole word only (not in catalog/catfish)
whole_word = re.findall(r'\bcat\b', text)
print(whole_word)  # ['cat']

# 'cat' anywhere
anywhere = re.findall(r'cat', text)
print(anywhere)  # ['cat', 'cat', 'cat']

# Words starting with 'cat'
starts_with = re.findall(r'\bcat\w*', text)
print(starts_with)  # ['cat', 'catalog', 'catfish']
```

#### 2.4.6 Groups and Alternation

| Pattern | Meaning | Example |
|---------|---------|---------|
| `(abc)` | Capture group | `(\w+)@(\w+)` captures parts |
| `(?:abc)` | Non-capturing group | Group without capturing |
| `a\|b` | OR (a or b) | `cat\|dog` matches either |

```python
import re

text = "john@gmail.com and jane@yahoo.org"

# Capture groups - extract parts
pattern = r'(\w+)@(\w+)\.(\w+)'
matches = re.findall(pattern, text)
print(matches)  # [('john', 'gmail', 'com'), ('jane', 'yahoo', 'org')]

# Alternation - either/or
text2 = "I have a cat and a dog"
animals = re.findall(r'cat|dog', text2)
print(animals)  # ['cat', 'dog']
```

#### 2.4.7 Common NLP Regex Patterns

**1. Email Addresses**
```python
# Basic email pattern
email = r'[\w\.-]+@[\w\.-]+'

# More strict email
email_strict = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
```

**2. URLs**
```python
# Basic URL pattern
url = r'https?://\S+'

# Example
text = "Visit https://example.com or http://test.org"
urls = re.findall(r'https?://\S+', text)
print(urls)  # ['https://example.com', 'http://test.org']
```

**3. Phone Numbers**
```python
# Various formats: 123-456-7890, (123) 456-7890, 123.456.7890
phone = r'[\d\(\)]{3}[\s\.\-]?\d{3}[\s\.\-]?\d{4}'

# Simpler: just digits with separators
phone_simple = r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
```

**4. Dates**
```python
# DD/MM/YYYY or DD-MM-YYYY
date = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'

text = "Born on 15/03/1990 and 2-5-2020"
dates = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
print(dates)  # ['15/03/1990', '2-5-2020']
```

**5. Hashtags and Mentions**
```python
# Twitter hashtags
hashtags = r'#\w+'

# Twitter mentions
mentions = r'@\w+'

text = "Hey @john check out #Python and #NLP"
print(re.findall(r'#\w+', text))   # ['#Python', '#NLP']
print(re.findall(r'@\w+', text))   # ['@john']
```

**6. Words with Specific Patterns**
```python
text = "running swimming eating sleeping"

# Words ending in 'ing'
ing_words = re.findall(r'\b\w+ing\b', text)
print(ing_words)  # ['running', 'swimming', 'eating', 'sleeping']

# Words starting with 's'
s_words = re.findall(r'\bs\w+', text)
print(s_words)  # ['swimming', 'sleeping']
```

**7. Numbers with Decimals**
```python
# Match integers and decimals
numbers = r'\d+\.?\d*'

text = "Price is 99.99 and quantity is 5"
nums = re.findall(r'\d+\.?\d*', text)
print(nums)  # ['99.99', '5']
```

**8. Extracting Quoted Text**
```python
# Text in double quotes
quoted = r'"([^"]*)"'

text = 'He said "hello" and "goodbye"'
quotes = re.findall(r'"([^"]*)"', text)
print(quotes)  # ['hello', 'goodbye']
```

#### 2.4.8 Python re Module Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `re.findall(pattern, text)` | Find ALL matches, return list | `re.findall(r'\d+', "a1b2")` → `['1','2']` |
| `re.search(pattern, text)` | Find FIRST match, return match object | `re.search(r'\d+', "a1b2").group()` → `'1'` |
| `re.match(pattern, text)` | Match at START only | `re.match(r'\d', "1abc")` → match |
| `re.sub(pattern, repl, text)` | Replace matches | `re.sub(r'\d', 'X', "a1b2")` → `'aXbX'` |
| `re.split(pattern, text)` | Split by pattern | `re.split(r'\s+', "a  b c")` → `['a','b','c']` |

```python
import re

text = "John: 25, Jane: 30, Bob: 22"

# findall - get all ages
ages = re.findall(r'\d+', text)
print(ages)  # ['25', '30', '22']

# search - get first age
first = re.search(r'\d+', text)
print(first.group())  # '25'

# sub - replace ages with XX
hidden = re.sub(r'\d+', 'XX', text)
print(hidden)  # 'John: XX, Jane: XX, Bob: XX'

# split - split by comma-space
parts = re.split(r',\s*', text)
print(parts)  # ['John: 25', 'Jane: 30', 'Bob: 22']
```

#### 2.4.9 Building Patterns Step-by-Step

**Example: Build an email pattern from scratch**

```
Goal: match john.doe@company.co.uk

Step 1: Username part (john.doe)
  - Letters, numbers, dots, underscores, hyphens
  - Pattern: [\w\.-]+

Step 2: @ symbol
  - Literal: @

Step 3: Domain part (company.co.uk)
  - Same characters as username
  - Pattern: [\w\.-]+

Combined: [\w\.-]+@[\w\.-]+
```

**Example: Build a date pattern**

```
Goal: match 15/03/2024 or 15-03-2024

Step 1: Day (1-2 digits)
  - Pattern: \d{1,2}

Step 2: Separator (/ or -)
  - Pattern: [/-]

Step 3: Month (1-2 digits)
  - Pattern: \d{1,2}

Step 4: Separator again
  - Pattern: [/-]

Step 5: Year (2 or 4 digits)
  - Pattern: \d{2,4}

Combined: \d{1,2}[/-]\d{1,2}[/-]\d{2,4}
```

#### 2.4.10 Regex Cheat Sheet for Exam

```
CHARACTERS:
  \w  = word char [a-zA-Z0-9_]     \d  = digit [0-9]
  \W  = non-word                   \D  = non-digit
  \s  = whitespace                 \S  = non-whitespace
  .   = any character              \.  = literal dot

QUANTIFIERS:
  +     = 1 or more                *   = 0 or more
  ?     = 0 or 1 (optional)        {n} = exactly n
  {n,}  = n or more                {n,m} = between n and m

ANCHORS:
  ^   = start of string            $   = end of string
  \b  = word boundary              \B  = non-word boundary

SETS:
  [abc]   = a, b, or c             [^abc] = NOT a, b, c
  [a-z]   = lowercase              [A-Z]  = uppercase
  [0-9]   = digits                 [a-zA-Z0-9] = alphanumeric

GROUPS:
  (abc)   = capture group          (?:abc) = non-capturing
  a|b     = a OR b

COMMON PATTERNS:
  Email:    [\w\.-]+@[\w\.-]+
  URL:      https?://\S+
  Hashtag:  #\w+
  Mention:  @\w+
  Date:     \d{1,2}[/-]\d{1,2}[/-]\d{2,4}
  Phone:    \d{3}[-.\s]?\d{3}[-.\s]?\d{4}
```

---

### 2.5 Complete Text Cleaning Function

```python
import string
import re

def clean_text(text):
    """Clean text: remove punctuation, lowercase, extract emails"""

    # 1. Extract emails BEFORE removing punctuation (@ is punctuation!)
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)

    # 2. Remove punctuation
    text_clean = text.translate(str.maketrans('', '', string.punctuation))

    # 3. Convert to lowercase
    text_lower = text_clean.lower()

    return text_lower, emails

# Usage
text = "Hello! Contact john@email.com for info."
cleaned, emails = clean_text(text)
print(f"Cleaned: {cleaned}")   # "hello contact johnemailcom for info"
print(f"Emails: {emails}")      # ['john@email.com']
```

---

## Module 3: Tokenization & Frequency

### 3.1 Tokenize Text into Words (Exam Task 1.3 - 5pts)

```python
from nltk import word_tokenize

text = "Hello world. How are you today?"

# Tokenize into words
tokens = word_tokenize(text)
print(tokens)  # ['Hello', 'world', '.', 'How', 'are', 'you', 'today', '?']

# Tokenize into sentences
from nltk import sent_tokenize
sentences = sent_tokenize(text)
print(sentences)  # ['Hello world.', 'How are you today?']
```

**Note:** `word_tokenize` keeps punctuation as separate tokens!

### 3.2 Clean Tokenization (words only, no punctuation)

```python
from nltk import word_tokenize

text = "Hello world! How are you?"
tokens = word_tokenize(text.lower())

# Filter: keep only alphabetic tokens
words = [token for token in tokens if token.isalpha()]
print(words)  # ['hello', 'world', 'how', 'are', 'you']
```

### 3.3 Count Word Frequency - FreqDist (Exam Task 1.4 - 5pts)

```python
from nltk import FreqDist, word_tokenize

text = "the cat sat on the mat the cat is happy"
tokens = word_tokenize(text.lower())
words = [t for t in tokens if t.isalpha()]

# Create frequency distribution
fdist = FreqDist(words)

# Get top 10 most common
top_10 = fdist.most_common(10)
print(top_10)
# [('the', 3), ('cat', 2), ('sat', 1), ('on', 1), ('mat', 1), ('is', 1), ('happy', 1)]

# Access specific word count
print(fdist['the'])  # 3

# Plot the distribution
fdist.plot(10)  # Shows bar chart of top 10 words
```

### 3.4 Conditional Frequency Distribution (Exam Task 1.5 - 10pts)

**What is CFD?** Counts frequency of one thing GIVEN another condition.

**Exam Task:** "Find and plot a conditional frequency distribution that shows how often each word length (in characters) appears for words starting with specific letters (e.g., 'a', 'b', 'c')."

```python
from nltk import ConditionalFreqDist, word_tokenize
import matplotlib.pyplot as plt

text = "apple banana avocado apricot berry cherry blueberry coconut"
tokens = word_tokenize(text.lower())
words = [t for t in tokens if t.isalpha()]

# CFD: condition = first letter, sample = word length
# Structure: (condition, sample)
cfd = ConditionalFreqDist(
    (word[0], len(word))  # (first_letter, word_length)
    for word in words
    if word[0] in 'abc'   # Only words starting with a, b, or c
)

# Print the CFD data
for letter in 'abc':
    print(f"Letter '{letter}': {dict(cfd[letter])}")

# Plot it
cfd.plot()
plt.show()
```

**Output explained:**
- For each starting letter (a, b, c), shows distribution of word lengths
- Example: words starting with 'a' might have lengths 5, 7, etc.

### 3.5 Full Example: Exam Task 1 (Parts 3-5)

```python
from nltk import FreqDist, ConditionalFreqDist, word_tokenize
import matplotlib.pyplot as plt

def analyze_text(text):
    # Task 1.3: Tokenize
    tokens = word_tokenize(text.lower())
    words = [t for t in tokens if t.isalpha()]
    print(f"Total tokens: {len(tokens)}")
    print(f"Alphabetic words: {len(words)}")

    # Task 1.4: Top 10 most frequent
    fdist = FreqDist(words)
    top_10 = fdist.most_common(10)
    print("\nTop 10 words:")
    for word, count in top_10:
        print(f"  {word}: {count}")

    # Task 1.5: CFD - word length by starting letter
    cfd = ConditionalFreqDist(
        (word[0], len(word))
        for word in words
        if word[0] in 'abc'
    )

    print("\nWord lengths by starting letter:")
    for letter in 'abc':
        print(f"  {letter}: {dict(cfd[letter])}")

    # Plot CFD
    cfd.plot()
    plt.title("Word Length Distribution by Starting Letter")
    plt.xlabel("Word Length")
    plt.ylabel("Frequency")
    plt.show()

    return words, top_10, cfd

# Usage
text = "your text here..."
words, top_10, cfd = analyze_text(text)
```

---

## Module 4: Corpora & WordNet

### 4.1 Gutenberg Corpus - Find Most Common Word (Exam Task 2.1 - 10pts)

```python
from nltk.corpus import gutenberg
from nltk import FreqDist

def find_most_common_in_gutenberg():
    # Get ALL words from Gutenberg corpus
    all_words = gutenberg.words()

    # Convert to lowercase and filter
    words = [w.lower() for w in all_words if w.isalpha()]

    # Create frequency distribution
    fdist = FreqDist(words)

    # Get the single most common word
    most_common = fdist.most_common(1)[0]  # Returns tuple (word, count)
    word, count = most_common

    print(f"Most common word: '{word}' with frequency {count}")
    return word, count

# Call it
word, freq = find_most_common_in_gutenberg()
```

**What's in Gutenberg?** Classic books like Emma, Moby Dick, Bible, etc.

### 4.2 WordNet - Find Synonyms and Antonyms (Exam Task 2.2 - 10pts)

```python
from nltk.corpus import wordnet

def find_synonyms_antonyms(word):
    """Find synonyms and antonyms using WordNet"""

    synonyms = []
    antonyms = []

    # Get all synsets (senses) of the word
    for syn in wordnet.synsets(word):
        # Get all lemmas (word forms) in this synset
        for lemma in syn.lemmas():
            # The lemma name is a synonym
            synonyms.append(lemma.name())

            # Check if this lemma has antonyms
            for ant in lemma.antonyms():
                antonyms.append(ant.name())

    # Remove duplicates
    synonyms = list(set(synonyms))
    antonyms = list(set(antonyms))

    return synonyms, antonyms

# Usage
word = "good"  # or whatever the most common word is
syns, ants = find_synonyms_antonyms(word)
print(f"Synonyms of '{word}': {syns}")
print(f"Antonyms of '{word}': {ants}")
```

### 4.3 Complete Exam Task 2 Solution

```python
from nltk.corpus import gutenberg, wordnet
from nltk import FreqDist

def common_word_analysis():
    """
    Exam Task 2:
    1. Find most common word in Gutenberg corpus
    2. Find its synonyms and antonyms using WordNet
    """

    # Step 1: Get most common word from Gutenberg
    all_words = gutenberg.words()
    words = [w.lower() for w in all_words if w.isalpha()]
    fdist = FreqDist(words)
    most_common_word, frequency = fdist.most_common(1)[0]

    print(f"Most common word: '{most_common_word}' (frequency: {frequency})")

    # Step 2: Find synonyms and antonyms
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(most_common_word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            for ant in lemma.antonyms():
                antonyms.append(ant.name())

    synonyms = list(set(synonyms))
    antonyms = list(set(antonyms))

    print(f"Synonyms: {synonyms}")
    print(f"Antonyms: {antonyms}")

    return most_common_word, frequency, synonyms, antonyms

# Run it
result = common_word_analysis()
```

---

## Module 5: POS Tagging

### 5.1 What is POS Tagging?

POS = Part of Speech. Tags each word with its grammatical role.

**Common Universal Tags:**
| Tag | Meaning | Example |
|-----|---------|---------|
| NOUN | Noun | dog, city |
| VERB | Verb | run, is |
| ADJ | Adjective | big, happy |
| ADV | Adverb | quickly |
| DET | Determiner | the, a, an |
| PRON | Pronoun | he, she |
| ADP | Preposition | in, on, at |
| CONJ | Conjunction | and, but |

### 5.2 Basic POS Tagging with NLTK

```python
from nltk import word_tokenize, pos_tag

sentence = "The quick brown fox jumps over the lazy dog."

# Step 1: Tokenize
tokens = word_tokenize(sentence)
print(tokens)  # ['The', 'quick', 'brown', ...]

# Step 2: POS tag
tagged = pos_tag(tokens)
print(tagged)
# [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ...]
```

**Note:** Default `pos_tag` uses Penn Treebank tags (DT, JJ, NN, VB, etc.)

### 5.3 Brown Corpus with Universal Tagset (Exam Task 3 - Part 1)

```python
from nltk.corpus import brown

# Get tagged sentences with UNIVERSAL tagset
tagged_sents = brown.tagged_sents(tagset='universal')

print(f"Total sentences: {len(tagged_sents)}")
print(f"First sentence: {tagged_sents[0]}")
# [('The', 'DET'), ('Fulton', 'NOUN'), ('County', 'NOUN'), ...]
```

### 5.4 Train a Bigram Tagger (Exam Task 3.1 - 10pts)

**What is a Bigram Tagger?**
- Uses the PREVIOUS tag to predict current tag
- Needs training data
- Often uses "backoff" chain: Bigram → Unigram → Default

```python
from nltk.corpus import brown
from nltk import DefaultTagger, UnigramTagger, BigramTagger

# Step 1: Get training data
tagged_sents = brown.tagged_sents(tagset='universal')

# Step 2: Split into train/test (90/10)
train_size = int(len(tagged_sents) * 0.9)
train_sents = tagged_sents[:train_size]
test_sents = tagged_sents[train_size:]

print(f"Training sentences: {len(train_sents)}")
print(f"Test sentences: {len(test_sents)}")

# Step 3: Build tagger chain (backoff pattern)
# If BigramTagger fails → try UnigramTagger → try DefaultTagger
t0 = DefaultTagger('NOUN')           # Fallback: guess NOUN
t1 = UnigramTagger(train_sents, backoff=t0)  # Uses word alone
t2 = BigramTagger(train_sents, backoff=t1)   # Uses previous tag + word

print("Bigram tagger trained!")
```

### 5.5 Tag a New Sentence (Exam Task 3.2 - 10pts)

```python
from nltk import word_tokenize

sentence = "The quick brown fox jumps over the lazy dog."

# Tokenize
tokens = word_tokenize(sentence)

# Tag with our trained bigram tagger
tagged_sentence = t2.tag(tokens)
print(tagged_sentence)
# [('The', 'DET'), ('quick', 'ADJ'), ('brown', 'ADJ'), ('fox', 'NOUN'),
#  ('jumps', 'VERB'), ('over', 'ADP'), ('the', 'DET'), ('lazy', 'ADJ'),
#  ('dog', 'NOUN'), ('.', '.')]
```

### 5.6 Calculate Accuracy (Exam Task 3.3 - 5pts)

```python
# Accuracy on test set
accuracy = t2.accuracy(test_sents)
print(f"Tagger accuracy: {accuracy:.4f}")
# Usually around 0.92-0.93 (92-93%)
```

### 5.7 Complete Exam Task 3 Solution

```python
from nltk.corpus import brown
from nltk import DefaultTagger, UnigramTagger, BigramTagger
from nltk import word_tokenize

def categorize_and_tag():
    """
    Exam Task 3:
    1. Train Bigram tagger on Brown corpus (universal tagset)
    2. Tag the sentence "The quick brown fox jumps over the lazy dog."
    3. Return tagged sentence and accuracy
    """

    # Step 1: Prepare data
    tagged_sents = brown.tagged_sents(tagset='universal')
    train_size = int(len(tagged_sents) * 0.9)
    train_sents = tagged_sents[:train_size]
    test_sents = tagged_sents[train_size:]

    # Step 2: Train tagger chain
    t0 = DefaultTagger('NOUN')
    t1 = UnigramTagger(train_sents, backoff=t0)
    t2 = BigramTagger(train_sents, backoff=t1)

    # Step 3: Tag the target sentence
    sentence = "The quick brown fox jumps over the lazy dog."
    tokens = word_tokenize(sentence)
    tagged_sentence = t2.tag(tokens)

    # Step 4: Calculate accuracy
    accuracy = t2.accuracy(test_sents)

    # Print results
    print("Tagged sentence:")
    print(tagged_sentence)
    print(f"\nTagger accuracy: {accuracy:.4f}")

    return tagged_sentence, accuracy

# Run it
tagged, acc = categorize_and_tag()
```

---

# DAY 2 - FINAL EXAM TOPICS

---

## Module 6: Feature Extraction

### 6.1 What is Feature Extraction?

Converting text into numbers so ML algorithms can use it.

Two main methods:
1. **Bag of Words (BoW)**: Count word occurrences
2. **TF-IDF**: Weight words by importance (rare words = more important)

### ([('The', 'DET'),
  ('quick', 'ADJ'),
  ('brown', 'ADJ'),
  ('fox', 'NOUN'),
  ('jumps', 'VERB'),
  ('over', 'ADP'),
  ('the', 'DET'),
  ('lazy', 'ADJ'),
  ('dog', 'NOUN'),
  ('.', '.')],
 0.9485446658703716) (Final Task 1 - option A)

```python
from sklearn.feature_extraction.text import CountVectorizer

# Sample documents (reviews)
documents = [
    "This movie is great",
    "This movie is terrible",
    "I love this film",
    "I hate this film"
]

# Create vectorizer
vectorizer = CountVectorizer()

# Fit and transform documents to matrix
X = vectorizer.fit_transform(documents)

# Display the matrix
print("Feature names (vocabulary):")
print(vectorizer.get_feature_names_out())
# ['film' 'great' 'hate' 'is' 'love' 'movie' 'terrible' 'this']

print("\nBoW Matrix:")
print(X.toarray())
# [[0 1 0 1 0 1 0 1]   <- "This movie is great"
#  [0 0 0 1 0 1 1 1]   <- "This movie is terrible"
#  [1 0 0 0 1 0 0 1]   <- "I love this film"
#  [1 0 1 0 0 0 0 1]]  <- "I hate this film"
```

### 6.3 TF-IDF with TfidfVectorizer (Final Task 1 - option B)

```python
from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "This movie is great",
    "This movie is terrible",
    "I love this film",
    "I hate this film"
]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform
X = vectorizer.fit_transform(documents)

# Display
print("Feature names:")
print(vectorizer.get_feature_names_out())

print("\nTF-IDF Matrix:")
print(X.toarray())
# Each value is now a weighted score instead of raw count
```

**TF-IDF vs BoW:**
- BoW: Just counts (word appears 3 times → 3)
- TF-IDF: Weights by rarity (common words like "the" get lower scores)

### 6.4 Display Feature Matrix Nicely (Final Task 1.2 - 5pts)

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

documents = ["This movie is great", "This movie is terrible"]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Create DataFrame for nice display
df = pd.DataFrame(
    X.toarray(),
    columns=vectorizer.get_feature_names_out(),
    index=[f"Doc {i+1}" for i in range(len(documents))]
)

print(df)
#           great        is     movie   terrible      this
# Doc 1  0.631667  0.449436  0.449436  0.000000  0.449436
# Doc 2  0.000000  0.449436  0.449436  0.631667  0.449436
```

---

## Module 7: Classification

### 7.1 Train/Test Split (Final Task 2.1 - 10pts)

```python
from sklearn.model_selection import train_test_split

# Your data
X = [...]  # Features (e.g., TF-IDF matrix)
y = [...]  # Labels (e.g., 'positive', 'negative')

# Split: 70% train, 30% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,      # 30% for testing
    random_state=42     # For reproducibility
)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
```

### 7.2 Naive Bayes Classifier - sklearn (Final Task 2.2 - 10pts)

```python
from sklearn.naive_bayes import MultinomialNB

# Create classifier
clf = MultinomialNB()

# Train on training data
clf.fit(X_train, y_train)

# Make predictions on test data
predictions = clf.predict(X_test)
```

### 7.3 Calculate Accuracy (Final Task 2.3 - 10pts)

```python
from sklearn.metrics import accuracy_score

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.4f}")
# or as percentage
print(f"Accuracy: {accuracy * 100:.2f}%")
```

### 7.4 Complete Final Task 2 Solution

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

def classify_reviews(reviews, labels):
    """
    Final Task 2:
    1. Split into 70% train, 30% test
    2. Train Naive Bayes classifier
    3. Calculate and return accuracy
    """

    # Step 1: Convert text to features (TF-IDF)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(reviews)
    y = labels

    # Step 2: Split data (70% train, 30% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")

    # Step 3: Train Naive Bayes
    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    # Step 4: Predict and calculate accuracy
    predictions = clf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy: {accuracy:.4f}")

    return accuracy

# Example usage
reviews = [
    "This movie is great, I loved it!",
    "Terrible film, waste of time",
    "Amazing acting and story",
    "Boring and predictable",
    "Best movie I've seen this year",
    "Would not recommend, very bad"
]
labels = ['positive', 'negative', 'positive', 'negative', 'positive', 'negative']

acc = classify_reviews(reviews, labels)
```

### 7.5 Alternative: NLTK Naive Bayes

```python
import nltk
import random

def nltk_naive_bayes(documents):
    """
    documents = list of (text, label) tuples
    Example: [("great movie", "pos"), ("bad film", "neg")]
    """

    # Feature extractor
    def document_features(document):
        words = set(document.lower().split())
        return {word: True for word in words}

    # Create feature sets
    featuresets = [(document_features(text), label) for (text, label) in documents]

    # Shuffle
    random.shuffle(featuresets)

    # Split
    split = int(len(featuresets) * 0.7)
    train_set = featuresets[:split]
    test_set = featuresets[split:]

    # Train
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    # Evaluate
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print(f"NLTK Naive Bayes Accuracy: {accuracy:.4f}")

    # Show most informative features
    classifier.show_most_informative_features(5)

    return classifier, accuracy
```

---

## Module 8: Chunking

### 8.1 What is Chunking?

Grouping words into phrases (like noun phrases, verb phrases).

**The Process:**
1. Tokenize sentence
2. POS tag each token
3. Apply grammar rules to create chunks

### 8.2 Basic Chunking Pattern (Final Task 3 - 10pts)

```python
from nltk import word_tokenize, pos_tag, RegexpParser

sentence = "The quick brown fox jumps over the lazy dog."

# Step 1: Tokenize
tokens = word_tokenize(sentence)
print("Tokens:", tokens)

# Step 2: POS tag
tagged = pos_tag(tokens)
print("Tagged:", tagged)
# [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ...]
```

### 8.3 Define Grammar for Noun Phrases

**Exam Task says:**
- Optional determiner (DT)
- Followed by any number of adjectives (JJ)
- Ending with a noun (NN)

```python
# Grammar pattern: NP: {<DT>?<JJ>*<NN>}
# Breakdown:
#   <DT>?  = optional determiner (? means 0 or 1)
#   <JJ>*  = zero or more adjectives (* means 0 or more)
#   <NN>   = exactly one noun

grammar = "NP: {<DT>?<JJ>*<NN>}"
```

### 8.4 Apply Grammar with RegexpParser

```python
from nltk import word_tokenize, pos_tag, RegexpParser

sentence = "The quick brown fox jumps over the lazy dog."

# Tokenize and tag
tokens = word_tokenize(sentence)
tagged = pos_tag(tokens)

# Define grammar
grammar = "NP: {<DT>?<JJ>*<NN>}"

# Create parser
parser = RegexpParser(grammar)

# Parse
result = parser.parse(tagged)

# Print tree structure
print(result)
```

**Output:**
```
(S
  (NP The/DT quick/JJ brown/JJ fox/NN)
  jumps/VBZ
  over/IN
  (NP the/DT lazy/JJ dog/NN)
  ./.)
```

### 8.5 Understanding Grammar Patterns

| Pattern | Meaning | Example Match |
|---------|---------|---------------|
| `<DT>` | Determiner | the, a, an |
| `<JJ>` | Adjective | quick, brown, lazy |
| `<NN>` | Noun (singular) | fox, dog, cat |
| `<VB>` | Verb (base) | jump, run |
| `<VBZ>` | Verb (3rd person) | jumps, runs |
| `<IN>` | Preposition | over, in, on |

| Modifier | Meaning |
|----------|---------|
| `?` | Optional (0 or 1) |
| `*` | Zero or more |
| `+` | One or more |
| `\|` | OR |

**More Grammar Examples:**
```python
# Noun phrases
"NP: {<DT>?<JJ>*<NN>}"

# Verb phrases
"VP: {<VB.*><NP>}"

# Multiple patterns
grammar = r"""
    NP: {<DT>?<JJ>*<NN>}
    VP: {<VB.*><NP>}
"""
```

### 8.6 Complete Final Task 3 Solution

```python
from nltk import word_tokenize, pos_tag, RegexpParser

def chunk_noun_phrases(sentence):
    """
    Final Task 3:
    Use NLTK to perform chunking to identify noun phrases.
    Grammar: optional DT + any number of JJ + NN
    """

    # Step 1: Tokenize
    tokens = word_tokenize(sentence)
    print("Tokens:", tokens)

    # Step 2: POS tag
    tagged = pos_tag(tokens)
    print("POS Tagged:", tagged)

    # Step 3: Define grammar
    # NP = optional determiner + zero or more adjectives + noun
    grammar = "NP: {<DT>?<JJ>*<NN>}"

    # Step 4: Create parser
    parser = RegexpParser(grammar)

    # Step 5: Parse
    result = parser.parse(tagged)

    # Print the parse tree
    print("\nParse Tree:")
    print(result)

    # Extract just the NP chunks
    print("\nNoun Phrases found:")
    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            print(f"  {subtree}")

    return result

# Run it
sentence = "The quick brown fox jumps over the lazy dog."
tree = chunk_noun_phrases(sentence)
```

**Expected Output:**
```
Tokens: ['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '.']
POS Tagged: [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN'), ('.', '.')]

Parse Tree:
(S
  (NP The/DT quick/JJ brown/JJ fox/NN)
  jumps/VBZ
  over/IN
  (NP the/DT lazy/JJ dog/NN)
  ./.)

Noun Phrases found:
  (NP The/DT quick/JJ brown/JJ fox/NN)
  (NP the/DT lazy/JJ dog/NN)
```

---

## Module 9: Cheat Sheet

### Quick Reference - All Imports

```python
# Standard
import re
import string
import random

# NLTK
import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk import FreqDist, ConditionalFreqDist
from nltk import RegexpParser
from nltk import DefaultTagger, UnigramTagger, BigramTagger
from nltk.corpus import gutenberg, brown, wordnet, stopwords

# Sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Visualization
import matplotlib.pyplot as plt
```

### Pattern Quick Reference

| Task | Code |
|------|------|
| Read file | `open(f).read()` |
| Remove punctuation | `text.translate(str.maketrans('', '', string.punctuation))` |
| Lowercase | `text.lower()` |
| Extract emails | `re.findall(r'[\w\.-]+@[\w\.-]+', text)` |
| Tokenize | `word_tokenize(text)` |
| Top N words | `FreqDist(words).most_common(N)` |
| CFD | `ConditionalFreqDist((condition, sample) for ...)` |
| Synsets | `wordnet.synsets(word)` |
| Synonyms | `[l.name() for s in synsets for l in s.lemmas()]` |
| Antonyms | `[a.name() for s in synsets for l in s.lemmas() for a in l.antonyms()]` |
| Train tagger | `BigramTagger(train, backoff=unigram)` |
| Tag sentence | `tagger.tag(tokens)` |
| Tagger accuracy | `tagger.accuracy(test_sents)` |
| TF-IDF | `TfidfVectorizer().fit_transform(docs)` |
| Train/test split | `train_test_split(X, y, test_size=0.3)` |
| Naive Bayes | `MultinomialNB().fit(X_train, y_train)` |
| Accuracy | `accuracy_score(y_test, predictions)` |
| Chunk NP | `RegexpParser("NP: {<DT>?<JJ>*<NN>}")` |

### Common POS Tags

| Tag | Meaning | Example |
|-----|---------|---------|
| DT | Determiner | the, a |
| JJ | Adjective | quick, brown |
| NN | Noun | fox, dog |
| NNS | Noun plural | foxes, dogs |
| NNP | Proper noun | John, Paris |
| VB | Verb base | run, jump |
| VBZ | Verb 3rd person | runs, jumps |
| VBD | Verb past | ran, jumped |
| IN | Preposition | over, in |
| RB | Adverb | quickly |

### Regex Quick Reference

| Pattern | Matches |
|---------|---------|
| `\w` | Word character (a-z, 0-9, _) |
| `\d` | Digit |
| `\s` | Whitespace |
| `.` | Any character |
| `+` | One or more |
| `*` | Zero or more |
| `?` | Zero or one |
| `[]` | Character class |
| `\b` | Word boundary |

### NLTK Downloads (Run Once)

```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('universal_tagset')
nltk.download('brown')
nltk.download('gutenberg')
nltk.download('wordnet')
nltk.download('stopwords')
```

---

## Exam Gotchas

1. **Extract emails BEFORE removing punctuation** (@ is punctuation!)

2. **Use `isalpha()` to filter tokens** - removes punctuation tokens

3. **CFD structure**: `(condition, sample)` - condition is what you group BY

4. **Tagger needs `tagset='universal'`** for universal tags

5. **TF-IDF needs `.toarray()`** to display as regular matrix

6. **`train_test_split` takes X, y** - features first, labels second

7. **Chunking grammar**: `{pattern}` for chunk, `}pattern{` for chink (exclude)

8. **Brown corpus uses Penn tags by default** - specify `tagset='universal'`
