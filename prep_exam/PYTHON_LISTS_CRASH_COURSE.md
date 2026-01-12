# Python Lists - Crash Course

---

## 1. What is a List?

A **list** is an ordered, mutable collection of items.

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]  # Can mix types
empty = []                         # Empty list
```

**Key Properties:**
- **Ordered** - items maintain their position
- **Mutable** - can add, remove, change items
- **Indexed** - access items by position number
- **Allows duplicates** - same value can appear multiple times

---

## 2. Accessing Elements (Indexing)

Lists are **zero-indexed** (first element is at position 0).

```python
fruits = ["apple", "banana", "cherry"]
#            0         1         2       (positive index)
#           -3        -2        -1       (negative index)

fruits[0]   # "apple"  (first)
fruits[1]   # "banana" (second)
fruits[-1]  # "cherry" (last)
fruits[-2]  # "banana" (second from end)
```

### Accessing Nested Lists

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

matrix[0]       # [1, 2, 3]  (first row)
matrix[0][0]    # 1          (first row, first element)
matrix[1][2]    # 6          (second row, third element)
matrix[-1][-1]  # 9          (last row, last element)
```

---

## 3. Slicing

Extract a portion of a list: `list[start:end:step]` (end is **exclusive**)

```python
nums = [0, 1, 2, 3, 4, 5]

nums[1:4]   # [1, 2, 3]      (index 1, 2, 3 - NOT 4)
nums[:3]    # [0, 1, 2]      (from start to index 2)
nums[3:]    # [3, 4, 5]      (from index 3 to end)
nums[::2]   # [0, 2, 4]      (every 2nd element)
nums[::-1]  # [5, 4, 3, 2, 1, 0]  (reversed)
nums[1:5:2] # [1, 3]         (index 1 to 4, every 2nd)
```

### Slicing Creates a Copy

```python
original = [1, 2, 3, 4, 5]
sliced = original[1:4]    # [2, 3, 4] - new list!

sliced[0] = 99            # Changes sliced only
print(original)           # [1, 2, 3, 4, 5] - unchanged
print(sliced)             # [99, 3, 4]
```

---

## 4. Modifying Lists

Lists are **mutable** (can be changed).

```python
fruits = ["apple", "banana", "cherry"]

# Change element
fruits[0] = "apricot"        # ["apricot", "banana", "cherry"]

# Add elements
fruits.append("date")        # Add to end
fruits.insert(1, "blueberry") # Insert at index 1

# Remove elements
fruits.remove("banana")      # Remove by value (first occurrence)
fruits.pop()                 # Remove & return last item
fruits.pop(0)                # Remove & return item at index 0
del fruits[1]                # Delete by index

# Clear all
fruits.clear()               # []
```

### Modifying with Slices

```python
nums = [0, 1, 2, 3, 4, 5]

nums[1:3] = [10, 20]        # [0, 10, 20, 3, 4, 5]
nums[1:3] = [10, 20, 30]    # [0, 10, 20, 30, 3, 4, 5] (can insert more)
nums[1:4] = []              # [0, 3, 4, 5] (delete via empty slice)
```

---

## 5. List Operations

```python
a = [1, 2, 3]
b = [4, 5, 6]

# Concatenation
a + b           # [1, 2, 3, 4, 5, 6]

# Repetition
a * 3           # [1, 2, 3, 1, 2, 3, 1, 2, 3]

# Length
len(a)          # 3

# Membership
2 in a          # True
7 in a          # False
7 not in a      # True

# Min/Max/Sum
min(a)          # 1
max(a)          # 3
sum(a)          # 6

# Sorting (returns new list)
sorted(a)                    # [1, 2, 3]
sorted(a, reverse=True)      # [3, 2, 1]
```

---

## 6. Iterating Over Lists

### Basic loop
```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
# apple
# banana
# cherry
```

### With index using enumerate()
```python
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry
```

### Iterating multiple lists with zip()
```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Alice: 85
# Bob: 92
# Charlie: 78
```

---

## 7. List Comprehensions (DETAILED)

List comprehensions are a concise way to create lists. They replace multi-line `for` loops with a single readable line.

### 7.1 Basic Syntax

```
[expression for item in iterable]
```

| Part | Meaning |
|------|---------|
| `expression` | What to put in the new list (can use `item`) |
| `item` | Variable name for each element |
| `iterable` | What to loop over (list, range, string, etc.) |

### 7.2 Simple Examples

```python
# Create list of squares
squares = [x**2 for x in range(5)]
# [0, 1, 4, 9, 16]

# Convert to uppercase
words = ["hello", "world"]
upper = [w.upper() for w in words]
# ["HELLO", "WORLD"]

# Get lengths
lengths = [len(w) for w in words]
# [5, 5]

# Extract first character
firsts = [w[0] for w in words]
# ['h', 'w']
```

### 7.3 Equivalent For Loop

Every list comprehension can be written as a for loop:

```python
# List comprehension
squares = [x**2 for x in range(5)]

# Equivalent for loop
squares = []
for x in range(5):
    squares.append(x**2)
```

**Visual mapping:**

```
    [  x**2   for   x   in   range(5)  ]
       ↓            ↓        ↓
    append       loop      iterable
              variable
```

### 7.4 Adding Conditions (Filtering)

```
[expression for item in iterable if condition]
```

The `if` filters which items are included:

```python
# Only even numbers
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Words longer than 3 characters
words = ["a", "be", "cat", "door", "elephant"]
long_words = [w for w in words if len(w) > 3]
# ["door", "elephant"]

# Only alphabetic tokens
tokens = ["hello", "123", "world", "!!!"]
alpha = [t for t in tokens if t.isalpha()]
# ["hello", "world"]
```

**Equivalent for loop:**

```python
# List comprehension
evens = [x for x in range(10) if x % 2 == 0]

# Equivalent for loop
evens = []
for x in range(10):
    if x % 2 == 0:
        evens.append(x)
```

### 7.5 Multiple Conditions

Use `and` / `or` for multiple conditions:

```python
# Even AND greater than 4
nums = [x for x in range(10) if x % 2 == 0 and x > 4]
# [6, 8]

# Starts with 'a' OR ends with 'e'
words = ["apple", "banana", "avocado", "grape", "orange"]
filtered = [w for w in words if w.startswith('a') or w.endswith('e')]
# ["apple", "avocado", "grape", "orange"]
```

### 7.6 If-Else in Expression (Ternary)

To transform values differently based on condition, put if-else in the **expression** part:

```
[true_value if condition else false_value for item in iterable]
```

```python
# Label numbers as even/odd
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ["even", "odd", "even", "odd", "even"]

# Replace negatives with zero
nums = [3, -1, 4, -5, 2]
non_neg = [x if x >= 0 else 0 for x in nums]
# [3, 0, 4, 0, 2]

# Capitalize first letter only
words = ["hello", "WORLD", "PyThOn"]
fixed = [w.capitalize() for w in words]
# ["Hello", "World", "Python"]
```

**Note the difference:**

```python
# if at END = FILTER (include or exclude)
[x for x in nums if x > 0]        # Only positive numbers

# if-else in EXPRESSION = TRANSFORM (change value)
[x if x > 0 else 0 for x in nums] # Replace negatives with 0
```

### 7.7 Nested Loops in Comprehensions

You can have multiple `for` clauses:

```
[expression for item1 in iterable1 for item2 in iterable2]
```

**Read left to right, like nested loops:**

```python
# All combinations
colors = ["red", "blue"]
sizes = ["S", "M", "L"]

combos = [(c, s) for c in colors for s in sizes]
# [('red', 'S'), ('red', 'M'), ('red', 'L'),
#  ('blue', 'S'), ('blue', 'M'), ('blue', 'L')]
```

**Equivalent for loop:**

```python
combos = []
for c in colors:          # First for (outer)
    for s in sizes:       # Second for (inner)
        combos.append((c, s))
```

### 7.8 Nested Loops with Conditions

```python
# Pairs where sum is even
pairs = [(x, y) for x in range(3) for y in range(3) if (x + y) % 2 == 0]
# [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
```

### 7.9 Flattening Nested Lists

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten to single list
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

**Read it as:**
```python
flat = []
for row in matrix:        # Outer loop
    for num in row:       # Inner loop
        flat.append(num)
```

### 7.10 Creating Nested Lists (2D Lists)

Use a comprehension **inside** a comprehension:

```python
# 3x3 matrix of zeros
matrix = [[0 for col in range(3)] for row in range(3)]
# [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# Multiplication table
table = [[i * j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# Transpose a matrix (swap rows and columns)
original = [[1, 2, 3], [4, 5, 6]]
transposed = [[row[i] for row in original] for i in range(3)]
# [[1, 4], [2, 5], [3, 6]]
```

### 7.11 The Single-Element List Trick (Variable Binding)

This trick creates a variable inside a comprehension:

```python
# Problem: Need to use computed value twice
[(word[0], word[0].upper()) for word in words]  # Computes word[0] twice

# Solution: Bind to variable using single-element list
[(char, char.upper()) for word in words for char in [word[0]]]
```

**How it works:**

```python
for word in words:
    for char in [word[0]]:    # List with ONE element
        # char = word[0], loops exactly once
        result.append((char, char.upper()))
```

### 7.12 Walrus Operator (Python 3.8+)

A cleaner alternative to the single-element list trick:

```python
# Using := (walrus operator) to assign and use
[(char := word[0], char.upper()) for word in words]
```

The `:=` assigns `word[0]` to `char` AND returns the value.

### 7.13 When to Use List Comprehensions

**Use when:**
- Creating a new list from an existing iterable
- Simple transformations or filters
- Code fits on one readable line

**Avoid when:**
- Logic is complex (use regular for loop)
- You need side effects (printing, modifying external state)
- Multiple statements per iteration
- Readability suffers

```python
# Good - simple and clear
squares = [x**2 for x in range(10)]

# Bad - too complex, use regular loop instead
result = [
    process(x)
    for x in data
    if validate(x) and x.category == 'A'
    for y in x.items
    if y.active
]
```

### 7.14 Common Patterns for NLP

```python
# Tokenize and lowercase
tokens = [word.lower() for word in text.split()]

# Filter stopwords
stopwords = {'the', 'a', 'an', 'is', 'are'}
filtered = [w for w in tokens if w not in stopwords]

# Keep only alphabetic words
alpha_only = [w for w in tokens if w.isalpha()]

# Get word lengths
lengths = [len(w) for w in tokens]

# Create (word, length) pairs
pairs = [(w, len(w)) for w in tokens]

# First letters of words starting with vowels
vowel_starts = [w[0] for w in tokens if w[0] in 'aeiou']

# Condition-Event pairs for CFD
cfd_pairs = [(w[0], len(w)) for w in tokens if w[0] in 'abc']
```

### 7.15 Summary Table

| Pattern | Syntax | Example |
|---------|--------|---------|
| Basic | `[expr for x in iter]` | `[x*2 for x in nums]` |
| Filter | `[expr for x in iter if cond]` | `[x for x in nums if x>0]` |
| Transform | `[a if cond else b for x in iter]` | `[x if x>0 else 0 for x in nums]` |
| Nested loop | `[expr for x in iter1 for y in iter2]` | `[(x,y) for x in a for y in b]` |
| Nested list | `[[expr for y in iter2] for x in iter1]` | `[[0]*3 for _ in range(3)]` |

---

## 8. The Single-Element List Trick (Expanded)

This is what confused you:

```python
for char in [word[0]]
```

### Breaking it down:

```python
word = "apple"
word[0]        # 'a' (a string/character)
[word[0]]      # ['a'] (a list containing one element)
```

### When you iterate over a single-element list:

```python
for char in ['a']:
    print(char)
# Output: a  (loops exactly once)
```

### Why would anyone do this?

It's a trick to **create a variable** inside a comprehension:

```python
# Instead of computing word[0] twice:
[(word[0], word[0].upper()) for word in words]

# You can "store" it in a variable:
[(char, char.upper()) for word in words for char in [word[0]]]
```

But for simple cases, it's overkill. Use the walrus operator `:=` in Python 3.8+ instead.

---

## 9. Common List Methods Reference

| Method | Description | Example |
|--------|-------------|---------|
| `append(x)` | Add to end | `[1,2].append(3)` → `[1,2,3]` |
| `extend(list)` | Add all items | `[1,2].extend([3,4])` → `[1,2,3,4]` |
| `insert(i, x)` | Insert at index | `[1,3].insert(1, 2)` → `[1,2,3]` |
| `remove(x)` | Remove first occurrence | `[1,2,2].remove(2)` → `[1,2]` |
| `pop(i)` | Remove & return at index | `[1,2,3].pop(1)` → returns `2` |
| `index(x)` | Find index of value | `[1,2,3].index(2)` → `1` |
| `count(x)` | Count occurrences | `[1,2,2,3].count(2)` → `2` |
| `sort()` | Sort in place | `[3,1,2].sort()` → `[1,2,3]` |
| `reverse()` | Reverse in place | `[1,2,3].reverse()` → `[3,2,1]` |
| `copy()` | Shallow copy | `b = a.copy()` |
| `clear()` | Remove all items | `[1,2,3].clear()` → `[]` |

---

## 10. Lists vs Strings

Both are sequences, but:

| Feature | List | String |
|---------|------|--------|
| Mutable | Yes | No |
| Syntax | `[a, b, c]` | `"abc"` |
| Elements | Any type | Characters only |
| Change item | `lst[0] = 'x'` | Not allowed |

```python
# String is immutable
s = "hello"
s[0] = "H"  # ERROR!

# List is mutable
lst = ["h", "e", "l", "l", "o"]
lst[0] = "H"  # OK! ["H", "e", "l", "l", "o"]
```

### Converting Between Them

```python
# String to list of characters
s = "hello"
lst = list(s)           # ['h', 'e', 'l', 'l', 'o']

# List to string
lst = ['h', 'e', 'l', 'l', 'o']
s = ''.join(lst)        # "hello"

# Split string to list of words
sentence = "hello world"
words = sentence.split()  # ['hello', 'world']

# Join words to string
words = ['hello', 'world']
sentence = ' '.join(words)  # "hello world"
```

---

## 11. List Copying (Shallow vs Deep)

### The Problem with Assignment

```python
a = [1, 2, 3]
b = a           # b points to SAME list!

b[0] = 99
print(a)        # [99, 2, 3] - a changed too!
```

### Shallow Copy

Creates new list, but nested objects are still shared:

```python
a = [1, 2, 3]
b = a.copy()    # or b = a[:] or b = list(a)

b[0] = 99
print(a)        # [1, 2, 3] - unchanged
```

### Deep Copy (for nested lists)

```python
import copy

a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)

b[0][0] = 99
print(a)        # [[1, 2], [3, 4]] - unchanged
```

---

## 12. Quick Mental Model

Think of a list as a **row of numbered boxes**:

```
Index:    0        1        2
       +--------+--------+--------+
       | apple  | banana | cherry |
       +--------+--------+--------+
```

- Each box has a number (index)
- You can look inside any box: `fruits[1]`
- You can replace contents: `fruits[1] = "blueberry"`
- You can add/remove boxes

---

## 13. Quick Reference: List Comprehension Anatomy

```
[ expression  for  item  in  iterable  if  condition ]
  ↑               ↑         ↑              ↑
  │               │         │              └── Optional filter
  │               │         └── What to loop over
  │               └── Loop variable name
  └── What to produce (uses loop variable)
```

**Read it as English:**

```python
[word.upper() for word in words if len(word) > 3]
```

*"Give me word.upper() FOR each word IN words IF len(word) > 3"*

---

*Created for IT 335 - NLP Course*
