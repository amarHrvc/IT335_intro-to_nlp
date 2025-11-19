# TravelPlanner Dataset Desdcription

## Overview
Document explains **TravelPlanner dataset**, its preprocessing steps, statistical analysis, and visualizations.
---

## 1. Dataset Source & Acquisition

**Dataset Name:** TravelPlanner  
**Source:** Hugging Face  
**Original Files:**
- `train.csv` (45 rows, 12 columns)
- `validation.csv` (180 rows, 11 columns)  
- `test.csv` (1000 rows, 7 columns)

**Why this dataset?**  
TravelPlanner contains realistic travel planning queries with multiple cities, dates, budgets, and difficulty levels. It is ideal to be used for Travel Itenerary Generator

---

## 2. Dataset Structure

### Train Dataset (45 rows)
**12 Columns:**
- `org` - Origin city
- `dest` - Destination city
- `days` - Trip duration (3-7 days)
- `visiting_city_number` - Number of cities to visit
- `date` - Start date
- `people_number` - Number of travelers
- `local_constraint` - Local constraints (e.g., cuisine preferences)
- `budget` - Budget amount
- `query` - Natural language travel request
- `level` - Difficulty level (easy/medium/hard)
- `annotated_plan` - Expert-annotated itinerary
- `reference_information` - Reference data (JSON format)

### Validation Dataset (180 rows)
**11 Columns:** Same as train, **there is no `annotated_plan`**

### Test Dataset (1000 rows)
**7 Columns:** Only core fields
- `org`, `dest`, `days`, `date`, `query`, `level`, `reference_information`

**Observation:** Test set has fewer columns because it's designed for model evaluation without giving away answers.

---

## 3. Data Preprocessing (`process_data_set.py`)

For data preprocessing [TravelPlannerProcessor](TravelPlannerProcessor.py) script is used 

### What Was Cleaned?

#### 3.1 Text Normalization
**Why?** Raw text has inconsistent capitalization, special characters, and whitespace.

**How it works:**
```python
def normalize_text(text):
    text = str(text).lower()          # Convert to lowercase
    text = text.strip()                # Remove leading/trailing spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove special chars
    return text
```

**Example:**
- Before: `"  New York!!! "`
- After: `"new york"`

**Applied to:** `query` field

---

#### 3.2 City Name Standardization
**Why?** City names were standardized for consistency

**How it works:**
```python
def normalize_cities(city):
    city = str(city).lower().strip().title()  # Title case
    return city if city else "unknown"
```

**Example:**
- Before: `"new york"`, `"NEW YORK"`, `"New york"`
- After: `"New York"` (consistent Title Case)

**it was applied to** `org`, `dest` fields

---

#### 3.3 Date Parsing
**Why?** Dates need to be in standard format for calculations.

**How it works:**
```python
def parse_date(date_str):
    return datetime.strptime(str(date_str), "%Y-%m-%d")
```

**Format:** `YYYY-MM-DD` (e.g., `2023-03-15`)

**Applied to:** `date` field

---

#### 3.4 Missing Value Handling
**Why?** Missing data can crash models or produce errors.

**Strategy:**
```python
df.fillna({
    'title': 'unknown',
    'description': 'no description',
    'org': 'unknown',
    'dest': 'unknown',
    'people_number': 1,
    'level': 'easy',
    'days': 1
}, inplace=True)
```

**Logic:**
- Text fields → `"unknown"` or `"no description"`
- Numeric fields → `1` (most common baseline)
- Difficulty → `"easy"` (most common)

---

#### 3.5 Expanded dataset with additional fields
**New columns which were added:**

| New Column | Calculation | Purpose |
|------------|-------------|---------|
| `query_normalized` | Cleaned query text | For NLP processing |
| `query_length_words` | Word count | Measure query complexity |
| `query_length_chars` | Character count | Text length analysis |
| `org_normalized` | Standardized origin | Consistent city names |
| `dest_normalized` | Standardized destination | Consistent city names |
| `data_split` | train/validation/test | Track data source |

---

## 4. Statistical Analysis (Jupyter Notebook)

### 4.1 Dataset Sizes
```
Train:      45 rows
Validation: 180 rows
Test:       1000 rows
Total:      1225 rows
```

**Why different sizes?**
- Small train set = Few examples for learning
- Medium validation = Check model performance
- Large test = Comprehensive evaluation

---

### 4.2 Trip Duration Distribution

**Analysis from Notebook:**
```python
train_df['days'].value_counts()
test_df['days'].value_counts()
```

**Findings:**
- **Most common:** 3-day trips
- **Range:** 3-7 days
- **Distribution:** Longer trips (5-7 days) are rarer

**Visualizations Created:** all visualizations are saved to results folder

**Interpretation:** Dataset focuses on short-to-medium trips.

---

### 4.3 Difficulty Levels

**Levels:**
- **Easy** - Single city, low budget, short trip
- **Medium** - Multiple cities, moderate complexity
- **Hard** - Many cities, high budget, complex logistics

**Visualization:** `difficulty_level.png`

**Purpose:** Models learn to handle varying complexity.

---

### 4.4 Group Size Analysis

**Field:** `people_number`

**Typical values:** 1-4 people

**Visualization:** `groups_size.png`

**Insight:** Most trips are solo or small groups (couples/families).

---

### 4.5 Top Cities

**Analysis:**
```python
train_df['org'].value_counts().head(10)  # Top origins
train_df['dest'].value_counts().head(10)  # Top destinations
```

**Visualizations:**
- `top_origin_cities.png`
- `top_destination_cities.png`

**Likely findings:** Popular cities like New York, Los Angeles, Chicago appear frequently.

---

## 5. Null Value Checks

**From Notebook:**
```python
print("Null values in Train dataset:")
print(train_df.isnull().sum())
```

**Result:** Script shows which columns have missing data (handled by preprocessing).

---

## 6. Data Type Verification

**Notebook check:**
```python
print(train_df.dtypes)
```

**Expected types:**
- `days`, `people_number`, `budget` → `int64`
- `org`, `dest`, `query` → `object` (string)
- `date` → `datetime` (after parsing)

**Why important?** Wrong types cause errors (e.g., trying to average strings).

---

## 7. Cleaned Dataset Output

**Location:** `TravelPlanner_cleaned/`

**Files:**
- `train_cleaned.csv`
- `validation_cleaned.csv`
- `test_cleaned.csv`


-
---

## 9. Conclusion

### Dataset Characteristics:
✅ **Size:** 1225 total records (small but focused)  
✅ **Quality:** Required cleaning (missing values, inconsistent formatting)  
✅ **Complexity:** Varies by difficulty level (easy/medium/hard)  
✅ **Real-world:** Represents actual travel planning scenarios

### Preprocessing Benefits:
✅ **Consistency:** Standardized text and city names  
✅ **Completeness:** No missing values after cleaning  
✅ **Features:** Added 6 new columns for analysis  
✅ **Reproducible:** Automated script for reuse