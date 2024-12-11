# Forward Chaining Inference System

## Overview

This project implements a **Forward Chaining Inference System**. It uses a knowledge base of facts and rules to determine if a given query is true or false. The system employs the forward chaining algorithm and provides a logical explanation via a proof tree.

---

## Features

- **Forward Chaining Algorithm**: Derives new facts iteratively based on the rules.
- **Proof Tree Generation**: Explains how the query is derived or why it is not.
- **Customizable Knowledge Base**: Add facts and rules easily via a text file.
- **Interactive Queries**: Input queries dynamically and get instant results.

---

## Files

- **`knowledge_base.txt`**: Contains facts, negative facts, and rules.
- **`forward_chaining.py`**: The Python script implementing the inference system.

---

## How to Use

1. **Set Up the Knowledge Base**:
   - Open `knowledge_base.txt`.
   - Add facts and rules in the following format:
     - **Positive facts**: `P`
     - **Negative facts**: `!D`
     - **Rules**: `P, Q -> R`

2. **Run the Script**:
   - Execute the Python script:
     ```bash
     python forward_chaining.py
     ```

3. **Input a Query**:
   - When prompted, type the query to check (e.g., `V`).

4. **View the Results**:
   - The script will indicate if the query is true or false.
   - If true, it also shows the proof tree.

---

## Example

### Knowledge Base (`knowledge_base.txt`):
```plaintext
P
R
P -> Q
Q -> V
R -> S
```

### Execution
```plaintext
Query ( Input From User): V
The query 'V' is derivable (True).

Proof tree:
V ↓
  Q ↓
    P

Other example. 
Query ( Input From User): D
The query 'D' is not derivable (False).
```

## Requirements
* Python 3.6 or later.
* No additional libraries required.
