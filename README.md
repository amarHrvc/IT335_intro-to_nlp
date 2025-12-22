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

---

## TIG (Travel Itinerary Generator) – Usage Guide

The **TIG_Implementation/** folder contains the main NLP project for a **Travel Itinerary Generator (TIG)** that parses natural-language travel requests and produces day-by-day itineraries grounded in the TravelPlanner dataset.

### 1. Run TIG from WSL

```bash
# Inside WSL, go to the project root
cd /mnt/d/_Learn/_IBU/IT_335/_test/IT335_intro-to_nlp

# Create and activate a Linux virtual environment
python3 -m venv linux-venv
source linux-venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r TIG_Implementation/requirements.txt

# Install spaCy English model used by the parser
python -m spacy download en_core_web_sm
```

### 2. Demo and Interactive Usage

```bash
cd TIG_Implementation
python main.py
```

Then choose a mode in the terminal:

- **Option 1 – Demo mode** (recommended for presentations):
  - Runs 3 predefined queries.
  - Prints structured itineraries to the console.
  - Saves JSON outputs to `TIG_Implementation/data/demo_output_*.json` and formatted text to `demo_output_*.txt`.
- **Option 2 – Interactive mode**:
  - You type your own queries in plain English (e.g. "3-day trip to Rome for 2 people, budget $2000").
  - Each itinerary is printed and saved as `interactive_output_*.json` and `.txt`.

These `.txt` files are convenient to copy into your NLP report or slides as qualitative examples.

### 3. Parser Evaluation (Quantitative Results)

To evaluate how accurately the **QueryParser** extracts destination, duration, budget, and people count:

```bash
cd TIG_Implementation/evaluation
source ../../linux-venv/bin/activate   # if not already active

# Quick environment check
python test_simple.py

# Main parser evaluation
python evaluate_parser.py
```

This creates three files in `TIG_Implementation/evaluation/results/`:

1. `parser_results_TIMESTAMP.json` – detailed per-query evaluation.
2. `parser_summary_TIMESTAMP.txt` – accuracy per field (good for the Results section).
3. `parser_comparison_TIMESTAMP.txt` – side-by-side ground truth vs parsed outputs.

### 4. Using Results in Your NLP Presentation

- Use **demo/interactive outputs** (`*.txt`) to show **qualitative** example itineraries.
- Use **parser_summary** to report **accuracy numbers** for destination/duration/budget/people.
- Optionally, follow `helpers/VISUALIZATION_HELPER_GUIDE.md` and `TIG_Implementation/evaluation/README.md` to turn these metrics into tables and charts for your report or slides.
