#!/usr/bin/env python3
"""
Basic NLP Project Example
This demonstrates simple text processing and analysis using NLTK
"""

def tokenize_text(text):
    """
    Simple tokenization function that splits text into words
    
    Args:
        text (str): Input text to tokenize
        
    Returns:
        list: List of tokens (words)
    """
    # Basic tokenization by splitting on whitespace and removing punctuation
    import re
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    tokens = text.split()
    return tokens


def analyze_text(text):
    """
    Analyze text and return basic statistics
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary containing text statistics
    """
    tokens = tokenize_text(text)
    
    stats = {
        'total_words': len(tokens),
        'unique_words': len(set(tokens)),
        'character_count': len(text),
        'average_word_length': sum(len(word) for word in tokens) / len(tokens) if tokens else 0
    }
    
    return stats


def main():
    """Main function to demonstrate NLP text processing"""
    
    # Sample text for analysis
    sample_text = """
    Natural Language Processing (NLP) is a subfield of artificial intelligence
    that focuses on the interaction between computers and humans through natural language.
    The ultimate objective of NLP is to read, decipher, understand, and make sense of
    human languages in a manner that is valuable.
    """
    
    print("=" * 60)
    print("NLP Project - Text Analysis Example")
    print("=" * 60)
    print("\nOriginal Text:")
    print(sample_text.strip())
    
    # Tokenize the text
    tokens = tokenize_text(sample_text)
    print("\n" + "-" * 60)
    print(f"Tokens (first 10): {tokens[:10]}")
    
    # Analyze the text
    stats = analyze_text(sample_text)
    print("\n" + "-" * 60)
    print("Text Statistics:")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value:.2f}" if isinstance(value, float) else f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
