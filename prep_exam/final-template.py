"""
NLP FINAL EXAM - SOLUTION TEMPLATE
===================================
Copy this file and modify as needed for your exam.

Tasks covered:
- Task 1: Feature Extraction (BoW/TF-IDF)
- Task 2: Train/Test Split + Naive Bayes Classification
- Task 3: Chunking (Noun Phrases)
"""

# ============================================================
# SETUP - Run this section first
# ============================================================
import nltk
import pandas as pd

# Download required data (run once, then comment out)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

from nltk import word_tokenize, pos_tag, RegexpParser

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score


# ============================================================
# SAMPLE DATA - Replace with actual exam data
# ============================================================

# Sample reviews for classification
SAMPLE_REVIEWS = [
    "This movie is great, I loved it!",
    "Terrible film, complete waste of time",
    "Amazing acting and wonderful story",
    "Boring and predictable, would not recommend",
    "Best movie I've seen this year",
    "Awful experience, very disappointing",
    "Fantastic cinematography and direction",
    "Poor script and bad acting",
    "Highly entertaining and fun to watch",
    "Dull and uninteresting from start to finish"
]

SAMPLE_LABELS = [
    'positive', 'negative', 'positive', 'negative', 'positive',
    'negative', 'positive', 'negative', 'positive', 'negative'
]


# ============================================================
# TASK 1: FEATURE EXTRACTION (BoW / TF-IDF)
# ============================================================

def task1_feature_extraction(reviews):
    """
    1. (10pts) Create BoW or TF-IDF matrix for reviews
    2. (5pts) Display the resulting feature matrix
    """

    print("=" * 60)
    print("TASK 1: FEATURE EXTRACTION")
    print("=" * 60)
    print()

    # --- Option A: Bag of Words (CountVectorizer) ---
    print("=== Option A: Bag of Words ===")

    bow_vectorizer = CountVectorizer()
    bow_matrix = bow_vectorizer.fit_transform(reviews)

    # Get feature names (vocabulary)
    feature_names = bow_vectorizer.get_feature_names_out()
    print(f"Vocabulary size: {len(feature_names)}")
    print(f"Feature names: {list(feature_names)}")
    print()

    # Display matrix
    print("BoW Matrix (raw):")
    print(bow_matrix.toarray())
    print()

    # Display as DataFrame (nicer)
    bow_df = pd.DataFrame(
        bow_matrix.toarray(),
        columns=feature_names,
        index=[f"Review {i+1}" for i in range(len(reviews))]
    )
    print("BoW Matrix (DataFrame):")
    print(bow_df)
    print()

    # --- Option B: TF-IDF (TfidfVectorizer) ---
    print("=== Option B: TF-IDF ===")

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(reviews)

    # Get feature names
    tfidf_features = tfidf_vectorizer.get_feature_names_out()
    print(f"Vocabulary size: {len(tfidf_features)}")
    print()

    # Display as DataFrame
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray().round(3),  # Round for readability
        columns=tfidf_features,
        index=[f"Review {i+1}" for i in range(len(reviews))]
    )
    print("TF-IDF Matrix (DataFrame):")
    print(tfidf_df)
    print()

    return {
        'bow_vectorizer': bow_vectorizer,
        'bow_matrix': bow_matrix,
        'tfidf_vectorizer': tfidf_vectorizer,
        'tfidf_matrix': tfidf_matrix
    }


# ============================================================
# TASK 2: MODEL TRAINING AND EVALUATION
# ============================================================

def task2_classification(reviews, labels):
    """
    1. (10pts) Split data: 70% train, 30% test
    2. (10pts) Train Naive Bayes classifier
    3. (10pts) Evaluate accuracy
    """

    print("=" * 60)
    print("TASK 2: MODEL SELECTION AND TRAINING")
    print("=" * 60)
    print()

    # --- Step 1: Feature Extraction (TF-IDF) ---
    print("=== Step 1: Feature Extraction ===")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(reviews)
    y = labels

    print(f"Feature matrix shape: {X.shape}")
    print(f"Number of samples: {X.shape[0]}")
    print(f"Number of features: {X.shape[1]}")
    print()

    # --- Task 2.1: Train/Test Split (10pts) ---
    print("=== Task 2.1: Train/Test Split (70/30) ===")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.3,      # 30% for testing
        random_state=42     # For reproducibility
    )

    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    print()

    # --- Task 2.2: Train Naive Bayes (10pts) ---
    print("=== Task 2.2: Training Naive Bayes ===")

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    print("Naive Bayes classifier trained successfully!")
    print()

    # --- Task 2.3: Evaluate Accuracy (10pts) ---
    print("=== Task 2.3: Evaluation ===")

    # Make predictions
    predictions = clf.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    print(f"Predictions: {list(predictions)}")
    print(f"Actual:      {list(y_test)}")
    print()
    print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print()

    return {
        'vectorizer': vectorizer,
        'classifier': clf,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'predictions': predictions,
        'accuracy': accuracy
    }


# ============================================================
# TASK 3: CHUNKING (NOUN PHRASES)
# ============================================================

def task3_chunking():
    """
    (10pts) Use NLTK to perform chunking to identify noun phrases.
    Sentence: "The quick brown fox jumps over the lazy dog."

    Grammar pattern:
    - Optional determiner (DT)
    - Followed by any number of adjectives (JJ)
    - Ending with a noun (NN)
    """

    print("=" * 60)
    print("TASK 3: CHUNKING (NOUN PHRASES)")
    print("=" * 60)
    print()

    sentence = "The quick brown fox jumps over the lazy dog."

    # --- Step 1: Tokenize ---
    print("=== Step 1: Tokenization ===")
    tokens = word_tokenize(sentence)
    print(f"Tokens: {tokens}")
    print()

    # --- Step 2: POS Tagging ---
    print("=== Step 2: POS Tagging ===")
    tagged = pos_tag(tokens)
    print(f"POS Tags: {tagged}")
    print()

    # Explain the tags
    print("Tag meanings:")
    for word, tag in tagged:
        if tag == 'DT':
            print(f"  {word}/{tag} - Determiner")
        elif tag == 'JJ':
            print(f"  {word}/{tag} - Adjective")
        elif tag == 'NN':
            print(f"  {word}/{tag} - Noun")
        elif tag == 'VBZ':
            print(f"  {word}/{tag} - Verb (3rd person)")
        elif tag == 'IN':
            print(f"  {word}/{tag} - Preposition")
    print()

    # --- Step 3: Define Grammar ---
    print("=== Step 3: Grammar Definition ===")

    # NP: optional DT + zero or more JJ + one NN
    grammar = "NP: {<DT>?<JJ>*<NN>}"

    print(f"Grammar: {grammar}")
    print("Pattern breakdown:")
    print("  <DT>? = optional determiner (0 or 1)")
    print("  <JJ>* = zero or more adjectives")
    print("  <NN>  = exactly one noun")
    print()

    # --- Step 4: Create Parser and Parse ---
    print("=== Step 4: Parsing ===")

    parser = RegexpParser(grammar)
    result = parser.parse(tagged)

    print("Parse Tree:")
    print(result)
    print()

    # --- Step 5: Extract Noun Phrases ---
    print("=== Noun Phrases Found ===")

    for subtree in result.subtrees():
        if subtree.label() == 'NP':
            # Get words in the chunk
            words = [word for word, tag in subtree.leaves()]
            print(f"  NP: {' '.join(words)}")
            print(f"      {subtree}")
    print()

    return {
        'tokens': tokens,
        'tagged': tagged,
        'grammar': grammar,
        'parse_tree': result
    }


# ============================================================
# ALTERNATIVE: NLTK Naive Bayes (instead of sklearn)
# ============================================================

def task2_nltk_naive_bayes(reviews, labels):
    """
    Alternative implementation using NLTK's Naive Bayes
    instead of sklearn's MultinomialNB.
    """
    import random

    print("=" * 60)
    print("TASK 2 (ALTERNATIVE): NLTK NAIVE BAYES")
    print("=" * 60)
    print()

    # Feature extractor function
    def document_features(document):
        words = set(document.lower().split())
        return {word: True for word in words}

    # Create feature sets
    documents = list(zip(reviews, labels))
    random.shuffle(documents)

    featuresets = [(document_features(text), label) for text, label in documents]

    # Split 70/30
    split_idx = int(len(featuresets) * 0.7)
    train_set = featuresets[:split_idx]
    test_set = featuresets[split_idx:]

    print(f"Training samples: {len(train_set)}")
    print(f"Test samples: {len(test_set)}")

    # Train NLTK Naive Bayes
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    # Evaluate
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print(f"Accuracy: {accuracy:.4f}")

    # Show informative features
    print("\nMost Informative Features:")
    classifier.show_most_informative_features(5)

    return classifier, accuracy


# ============================================================
# MAIN - Run all tasks
# ============================================================

if __name__ == "__main__":
    print()
    print("*" * 60)
    print("NLP FINAL EXAM - RUNNING ALL TASKS")
    print("*" * 60)
    print()

    # Task 1: Feature Extraction
    result1 = task1_feature_extraction(SAMPLE_REVIEWS)

    # Task 2: Classification
    result2 = task2_classification(SAMPLE_REVIEWS, SAMPLE_LABELS)

    # Task 3: Chunking
    result3 = task3_chunking()

    # Optional: NLTK Naive Bayes alternative
    # result2_alt = task2_nltk_naive_bayes(SAMPLE_REVIEWS, SAMPLE_LABELS)

    print("*" * 60)
    print("ALL TASKS COMPLETED")
    print("*" * 60)
