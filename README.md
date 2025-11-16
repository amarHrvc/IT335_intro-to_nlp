# IT335_intro-to_nlp
Introduction to Natural Language Processing (NLP) subject

## Project Setup

This project is set up as a Python-based NLP project with a virtual environment for dependency management.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/amarHrvc/IT335_intro-to_nlp.git
   cd IT335_intro-to_nlp
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Linux/Mac:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

After activating the virtual environment, you can run the main script:

```bash
python main.py
```

### Project Structure

```
IT335_intro-to_nlp/
├── .gitignore          # Excludes virtual environment and temporary files
├── requirements.txt    # Python dependencies
├── main.py            # Main NLP example script
└── README.md          # This file
```

### Included Libraries

- **nltk**: Natural Language Toolkit for text processing
- **spacy**: Industrial-strength NLP library
- **textblob**: Simplified text processing
- **scikit-learn**: Machine learning library
- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **matplotlib/seaborn**: Data visualization

### Deactivating the Virtual Environment

When you're done working on the project:

```bash
deactivate
```

### Notes

- The virtual environment (`venv/`) is excluded from version control via `.gitignore`
- Always activate the virtual environment before working on the project
- Keep `requirements.txt` updated when adding new dependencies
