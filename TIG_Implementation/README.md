# Travel Itinerary Generator (TIG) - Milestone 3

**Course:** IT_335 - Introduction to Natural Language Processing  
**Deadline:** November 24, 2025  
**Status:** Implementation Complete ✅

---

## 📋 Overview

The Travel Itinerary Generator (TIG) is an NLP-powered system that:
1. Parses natural language travel requests using **spaCy NER**
2. Generates day-by-day itineraries using **LLM-based planning**
3. Produces complete travel plans with activities, meals, and accommodations

**Key Features:**
- ✅ Natural language query understanding
- ✅ Entity extraction (destination, dates, budget, interests)
- ✅ Few-shot prompting with dataset examples
- ✅ Grounding to TravelPlanner dataset
- ✅ Multiple LLM provider support (OpenAI, Claude, Ollama)
- ✅ Rule-based fallback (works without API keys)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+
python --version

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Running the Demo

```bash
# Navigate to project folder
cd TIG_Implementation

# Run main demo (no API keys needed)
python main.py

# Select option 1 for demo mode
```

**Output:** Generates 3 example itineraries and saves as JSON files.

---

## 📁 Project Structure

```
TIG_Implementation/
├── agents/
│   ├── query_parser.py          # NLU component (spaCy + optional LLM)
│   ├── planner.py               # Itinerary generation agent
│   ├── llm_provider.py          # OpenAI/Claude abstraction
│   └── llm_provider_ollama.py   # Ollama (free local LLM) support
├── utils/
│   └── data_loader.py           # TravelPlanner dataset interface
├── tests/
│   ├── test_parser.py           # Query parser tests
│   ├── test_planner.py          # Planner tests
│   └── test_data.py             # Data loader tests
├── main.py                      # Main orchestrator & demo
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

---

## 🔧 System Components

### 1. Query Parser (agents/query_parser.py)

**Purpose:** Extract structured information from natural language

**Input:**
```
"Plan a 3-day trip to Rome for 2 people with $2000 budget. We love history."
```

**Output:**
```json
{
  "destination": "Rome",
  "duration": 3,
  "people_number": 2,
  "budget": 2000,
  "interests": ["history"]
}
```

**Implementation:**
- Stage 1: spaCy NER for entity extraction
- Stage 2: Rule-based structuring
- Optional: LLM-based parsing for complex queries

**Key Features:**
- Extracts: destination, duration, dates, budget, people, interests
- Handles variations ("3 days", "weekend", "next month")
- Normalizes entities to standard format

---

### 2. Travel Dataset (utils/data_loader.py)

**Purpose:** Interface to TravelPlanner benchmark dataset

**Functionality:**
- Loads train/validation/test splits
- Retrieves similar queries (for few-shot prompting)
- Provides city information (hotels, restaurants, attractions)
- Validates locations against dataset

**Dataset Statistics:**
- Train: 45 annotated query-plan pairs
- Validation: 180 queries
- Test: 1000 queries
- Cities: 50+ destinations

---

### 3. Itinerary Planner (agents/planner.py)

**Purpose:** Generate day-by-day travel plans

**Algorithm:**
1. Retrieve similar examples from dataset (RAG)
2. Build few-shot prompt with examples
3. Generate itinerary using LLM
4. Ground to dataset (validate locations)
5. Return structured plan

**Output Format:**
```json
{
  "days": [
    {
      "day": 1,
      "date": "2024-03-15",
      "morning": {"time": "09:00", "activity": "Colosseum", "type": "attraction"},
      "lunch": {"time": "13:00", "restaurant": "Trattoria Roma"},
      "afternoon": {"time": "15:00", "activity": "Roman Forum"},
      "dinner": {"time": "19:00", "restaurant": "Ristorante Aroma"},
      "accommodation": "Hotel Centrale"
    }
  ],
  "budget_breakdown": {
    "accommodation": 360,
    "food": 255,
    "activities": 105,
    "total": 720
  }
}
```

---

### 4. Main Orchestrator (main.py)

**Purpose:** Coordinate all components

**Workflow:**
```
User Query → Parser → Planner → Itinerary
```

**Modes:**
- **Demo Mode:** Runs 3 predefined queries
- **Interactive Mode:** User enters custom queries

---

## 🤖 LLM Provider Options

### Option 1: Rule-Based (No API Keys) ✅ **RECOMMENDED FOR DEMO**

```python
system = TIGSystem(use_llm=False)
```

**Pros:**
- ✅ Works immediately, no setup
- ✅ Fast, consistent results
- ✅ No API costs
- ✅ Good for demonstration

**Cons:**
- ❌ Less flexible than LLM
- ❌ Template-based outputs

---

### Option 2: Ollama (Free Local LLM)

**Setup:**
```bash
# 1. Download Ollama
# Visit: https://ollama.ai/download

# 2. Install a model
ollama pull llama2

# 3. Start server
ollama serve
```

**Usage:**
```python
system = TIGSystem(use_llm=True)
# Will auto-detect Ollama
```

**Pros:**
- ✅ Free and private
- ✅ No API limits
- ✅ Good quality (Llama2, Mistral)

**Cons:**
- ❌ Requires local installation
- ❌ Needs GPU for speed

---

### Option 3: OpenAI/Claude (Requires API Key)

**Setup:**
```bash
# Copy .env.example to .env
cp .env.example .env

# Add your API key
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=your-key-here
```

**Usage:**
```python
from agents.planner import ItineraryPlanner

planner = ItineraryPlanner(dataset, llm_provider="openai")
# OR
planner = ItineraryPlanner(dataset, llm_provider="claude")
```

**Pros:**
- ✅ Best quality
- ✅ Most flexible

**Cons:**
- ❌ Costs money
- ❌ Requires internet

---

## 📊 Testing

Run all tests:
```bash
# Test query parser
python -m tests.test_parser

# Test data loader
python -m tests.test_data

# Test planner
python -m tests.test_planner
```

---

## 📝 Example Usage

### Programmatic Usage

```python
from main import TIGSystem

# Initialize system (use_llm=False for rule-based fallback)
system = TIGSystem(use_llm=False)

# Generate itinerary
query = "3-day trip to Rome for 2 people, budget $2000"
itinerary = system.generate_itinerary(query)

# Print result
system.print_itinerary(itinerary)

# Save to file
import json
with open('itinerary.json', 'w') as f:
    json.dump(itinerary, f, indent=2)
```

---

## 🔬 Technical Details

### Dataset
- **Source:** TravelPlanner (Xie et al., 2024)
- **Link:** https://huggingface.co/datasets/osunlp/TravelPlanner
- **Paper:** https://arxiv.org/abs/2402.01622

### NLP Techniques
- Named Entity Recognition (spaCy)
- Few-shot prompting
- Retrieval-Augmented Generation (RAG)
- Grounding to prevent hallucination

### Dependencies
- spaCy (NER)
- OpenAI / Anthropic (LLM APIs)
- Requests (Ollama)
- Pandas (data processing)
- Python-dotenv (config)

---

## ⚠️ Known Limitations

1. **No Constraint Validator:** Due to time constraints, constraint validation is implemented as rule-based post-processing rather than an iterative agent. This is documented as future work.

2. **Limited Real-Time Data:** System uses static TravelPlanner dataset. Does not query real APIs (flights, hotels) for current prices/availability.

3. **English Only:** Currently only supports English queries.

4. **Simple Feedback Loop:** No interactive refinement implemented yet (future work).

---

## 🚧 Future Work

1. **Constraint Validator Agent:** Implement iterative validation and refinement loop
2. **Real-Time Data Integration:** Query flight/hotel APIs for current information
3. **Multi-Language Support:** Add support for other languages
4. **User Feedback Loop:** Allow users to refine itineraries interactively
5. **Evaluation Framework:** Comprehensive metrics for itinerary quality

---

## 📚 References

1. Xie et al. (2024). TravelPlanner: A Benchmark for Real-World Planning with Language Agents. arXiv:2402.01622

2. Liu et al. (2024). LARA: Linguistic-Adaptive Retrieval-Augmentation for Multi-Turn Intent Classification. EMNLP 2024.

3. Song et al. (2023). LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models. ICCV 2023.

---

## 👨‍💻 Author

**Student:** [Your Name]  
**Course:** IT_335 - Natural Language Processing  
**Instructor:** Amar Hajrovic  
**Semester:** Fall 2024/2025

---

## 📄 License

Academic project for educational purposes.  
Dataset: CC-BY-4.0 (TravelPlanner)

---

**Last Updated:** November 23, 2025  
**Version:** Milestone 3 - Implementation Complete ✅

---

### Option 2: Ollama (Free Local LLM)

**Setup:**
```bash
# 1. Download Ollama
# Visit: https://ollama.ai/download

# 2. Install a model
ollama pull llama2

# 3. Start server
ollama serve
```

**Usage:**
```python
system = TIGSystem(use_llm=True)
# Will auto-detect Ollama
```

**Pros:**
- ✅ Free and private
- ✅ No API limits
- ✅ Good quality (Llama2, Mistral)

**Cons:**
- ❌ Requires local installation
- ❌ Needs GPU for speed

---

### Option 3: OpenAI/Claude (Requires API Key)

**Setup:**
```bash
# Copy .env.example to .env
cp .env.example .env

# Add your API key
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=your-key-here
```

**Usage:**
```python
from agents.planner import ItineraryPlanner

planner = ItineraryPlanner(dataset, llm_provider="openai")
# OR
planner = ItineraryPlanner(dataset, llm_provider="claude")
```

**Pros:**
- ✅ Best quality
- ✅ Most flexible

**Cons:**
- ❌ Costs money
- ❌ Requires internet

---

## 📊 Testing

Run all tests:
```bash
# Test query parser
python -m tests.test_parser

# Test data loader
python -m tests.test_data

# Test planner
python -m tests.test_planner
```

---

## 📝 Example Usage

### Programmatic Usage

```python
from main import TIGSystem

# Initialize system (use_llm=False for rule-based fallback)
system = TIGSystem(use_llm=False)

# Generate itinerary
query = "3-day trip to Rome for 2 people, budget $2000"
itinerary = system.generate_itinerary(query)

# Print result
system.print_itinerary(itinerary)

# Save to file
import json
with open('itinerary.json', 'w') as f:
    json.dump(itinerary, f, indent=2)
```

---

## 🔬 Technical Details

### Dataset
- **Source:** TravelPlanner (Xie et al., 2024)
- **Link:** https://huggingface.co/datasets/osunlp/TravelPlanner
- **Paper:** https://arxiv.org/abs/2402.01622

### NLP Techniques
- Named Entity Recognition (spaCy)
- Few-shot prompting
- Retrieval-Augmented Generation (RAG)
- Grounding to prevent hallucination

### Dependencies
- spaCy (NER)
- OpenAI / Anthropic (LLM APIs)
- Requests (Ollama)
- Pandas (data processing)
- Python-dotenv (config)

---

## ⚠️ Known Limitations

1. **No Constraint Validator:** Due to time constraints, constraint validation is implemented as rule-based post-processing rather than an iterative agent. This is documented as future work.

2. **Limited Real-Time Data:** System uses static TravelPlanner dataset. Does not query real APIs (flights, hotels) for current prices/availability.

3. **English Only:** Currently only supports English queries.

4. **Simple Feedback Loop:** No interactive refinement implemented yet (future work).

---

## 🚧 Future Work

1. **Constraint Validator Agent:** Implement iterative validation and refinement loop
2. **Real-Time Data Integration:** Query flight/hotel APIs for current information
3. **Multi-Language Support:** Add support for other languages
4. **User Feedback Loop:** Allow users to refine itineraries interactively
5. **Evaluation Framework:** Comprehensive metrics for itinerary quality

---

## 📚 References

1. Xie et al. (2024). TravelPlanner: A Benchmark for Real-World Planning with Language Agents. arXiv:2402.01622

2. Liu et al. (2024). LARA: Linguistic-Adaptive Retrieval-Augmentation for Multi-Turn Intent Classification. EMNLP 2024.

3. Song et al. (2023). LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models. ICCV 2023.

---

## 👨‍💻 Author

**Student:** [Your Name]  
**Course:** IT_335 - Natural Language Processing  
**Instructor:** Amar Hajrovic  
**Semester:** Fall 2024/2025

---

## 📄 License

Academic project for educational purposes.  
Dataset: CC-BY-4.0 (TravelPlanner)

---

**Last Updated:** November 23, 2025  
**Version:** Milestone 3 - Implementation Complete ✅
