# NLP Exam - Lecture Material Mapping

## MIDTERM EXAM TOPICS

### 1. Text File I/O and Cleaning (Regex, Punctuation Removal, Lowercasing)
- **Primary Source:** `_exam_prep/midterm.ipynb` (cells 1-6)
- **Secondary:** `_week_4/4.1 ProcessingRawText.ipynb`
- **Key Functions:**
  - `with open('filename.txt', 'r') as f: text = f.read()`
  - `text.translate(str.maketrans('', '', string.punctuation))`
  - `text.lower()`
  - `re.findall(pattern, text)`

### 2. Tokenization and Frequency Analysis
- **Primary Source:** `_exam_prep/midterm.ipynb` (cells 13-20)
- **Secondary:** `_week_2/Lab 2 - Language Processing and Python.ipynb` (cells 21-25)
- **Key Functions:**
  - `nltk.word_tokenize(text)`
  - `FreqDist(tokens)`
  - `fdist.most_common(n)`
  - `fdist.plot(n)`

### 3. Email Extraction with Regex
- **Primary Source:** `_exam_prep/midterm.ipynb` (cells 7-10)
- **Key Pattern:**
  - `email_pattern = r'[\w\.]+@[\w\.]+'`
  - `re.findall(email_pattern, text)`

### 4. Conditional Frequency Distributions and Plotting
- **Primary Source:** `_exam_prep/midterm.ipynb` (cells 21-24)
- **Secondary:** `_week_3/Lab 3 - Accessing Text Corpora and Lexical Resources.ipynb` (cell 16)
- **Key Functions:**
  - `nltk.ConditionalFreqDist((condition, event) for ...)`
  - `cfd.plot()`
  - `cfd.tabulate()`

### 5. NLTK Corpus Operations (Gutenberg, Brown)
- **Primary Source:** `_week_3/Lab 3 - Accessing Text Corpora and Lexical Resources.ipynb` (cells 3-27)
- **Key Functions:**
  - `from nltk.corpus import gutenberg, brown`
  - `gutenberg.fileids()`
  - `gutenberg.words('austen-persuasion.txt')`
  - `brown.categories()`
  - `brown.tagged_sents(tagset='universal')`
  - `brown.words(categories='news')`

### 6. WordNet (Synonyms/Antonyms)
- **Primary Source:** `_week_3/Lab 3 - Accessing Text Corpora and Lexical Resources.ipynb` (cells 37-54)
- **Key Functions:**
  - `from nltk.corpus import wordnet as wn`
  - `wn.synsets('word')`
  - `synset.lemmas()`
  - `lemma.name()` - for synonyms
  - `lemma.antonyms()` - for antonyms
  - `synset.definition()`
  - `synset.hypernyms()`, `synset.hyponyms()`

### 7. POS Tagging with Bigram Tagger
- **Primary Source:** `_week_5/Lab 5 - Categorizing and Tagging Words & N-gram Tagging.pdf`
- **Key Functions:**
  - `from nltk.tag import UnigramTagger, BigramTagger, DefaultTagger`
  - `from nltk.corpus import brown`
  - `brown.tagged_sents(tagset='universal')`
  - Train/test split: `train_sents = tagged_sents[:size]`, `test_sents = tagged_sents[size:]`
  - `tagger = BigramTagger(train_sents, backoff=unigram_tagger)`
  - `tagger.accuracy(test_sents)`

### 8. Tagger Training and Accuracy Evaluation
- **Primary Source:** `_week_5/Lab 5 - Categorizing and Tagging Words & N-gram Tagging.pdf`
- **Key Pattern:**
  ```python
  # Backoff chain: Bigram -> Unigram -> Default
  t0 = DefaultTagger('NN')
  t1 = UnigramTagger(train_sents, backoff=t0)
  t2 = BigramTagger(train_sents, backoff=t1)
  accuracy = t2.accuracy(test_sents)
  ```

---

## FINAL EXAM TOPICS

### 1. Feature Extraction (BoW, TF-IDF)
- **Primary Source:** `_week_6/Lab 6 - Introduction to Machine Learning.ipynb` (cells 15, 24)
- **Secondary:** `_week_6/Lab_6.ipynb` (cells 10, 16)
- **Key Functions:**
  - `from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer`
  - `vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')`
  - `X = vectorizer.fit_transform(texts)`
  - `vectorizer.get_feature_names_out()`

### 2. Train/Test Split
- **Primary Source:** `_week_6/Lab 6 - Introduction to Machine Learning.ipynb` (cell 12)
- **Key Functions:**
  - `from sklearn.model_selection import train_test_split`
  - `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)`

### 3. Naive Bayes Classification
- **Primary Source:** `_week_6/Lab 6 - Introduction to Machine Learning.ipynb`
- **Note:** Lectures use LogisticRegression, but Naive Bayes follows same pattern:
  - `from sklearn.naive_bayes import MultinomialNB`
  - `clf = MultinomialNB()`
  - `clf.fit(X_train, y_train)`
  - `predictions = clf.predict(X_test)`

### 4. Model Evaluation (Accuracy)
- **Primary Source:** `_week_6/Lab 6 - Introduction to Machine Learning.ipynb` (cells 18, 32)
- **Key Functions:**
  - `from sklearn.metrics import classification_report, accuracy_score, confusion_matrix`
  - `print(classification_report(y_test, predictions))`
  - `accuracy_score(y_test, predictions)`
  - `ConfusionMatrixDisplay.from_predictions(y_test, predictions)`

### 5. Chunking with Grammar Rules
- **Primary Source:** `_week_8/8. Extracting Information from Text.ipynb` (cells 3-20)
- **Key Functions:**
  - `grammar = "NP: {<DT>?<JJ>*<NN>}"`
  - `cp = nltk.RegexpParser(grammar)`
  - `result = cp.parse(tagged_sentence)`

### 6. Noun Phrase Extraction
- **Primary Source:** `_week_8/8. Extracting Information from Text.ipynb`
- **Key Pattern:**
  ```python
  grammar = r"NP: {<DT|PP\$>?<JJ>*<NN>}"
  cp = nltk.RegexpParser(grammar)
  for sent in tagged_sents:
      tree = cp.parse(sent)
      for subtree in tree.subtrees():
          if subtree.label() == 'NP':
              print(subtree)
  ```

---

## QUICK REFERENCE: File Locations

| Topic | Primary File | Cells/Pages |
|-------|-------------|-------------|
| File I/O & Cleaning | midterm.ipynb | 1-6 |
| Tokenization | midterm.ipynb | 13-20 |
| Email Regex | midterm.ipynb | 7-10 |
| CFD Plotting | midterm.ipynb | 21-24 |
| Gutenberg/Brown | Lab 3.ipynb | 3-27 |
| WordNet | Lab 3.ipynb | 37-54 |
| POS Tagging | Lab 5.pdf | Pages 5, 7, 9, 12 |
| TF-IDF/BoW | Lab 6.ipynb | 15, 24 |
| Train/Test Split | Lab 6.ipynb | 12 |
| Classification | Lab 6.ipynb | 15-18 |
| Chunking | Week 8.ipynb | 3-20 |
