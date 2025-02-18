```markdown
# Forward Chaining Inference System

## Overview

This repository contains two implementations of a **Forward Chaining Inference System** that uses propositional predicate logic to deduce new facts from a provided knowledge base. Both versions accept a knowledge base of facts and rules and then interactively answer whether a given query is derivable. You can choose between:

- A version that displays the sequence of applied rules and derived facts.
- A version that generates a proof tree to explain the inference process.

## Features

- **Forward Chaining Algorithm:** Iteratively deduces new facts based on provided rules.
- **Interactive Querying:** Input queries dynamically to check if a fact is derivable.
- **Customizable Knowledge Base:** Easily edit the text files to add your own facts and rules.
- **Detailed Inference Explanation:** Choose between a rule trace or a full proof tree demonstration.

## Files

- **`knowledge_base.txt`**: Sample knowledge base for the proof tree version.
- **`forward_chaining.py`**: Python script implementing the forward chaining algorithm with proof tree generation.
- **`knowledge_base_2.txt`**: Sample knowledge base for the rule trace version.
- **`forward_chaining_2.py`**: Python script implementing the forward chaining algorithm with applied rule trace.

## How to Use

### Setting Up the Knowledge Base

Edit the appropriate knowledge base file (either `knowledge_base.txt` or `knowledge_base_2.txt`) with your facts and rules. The expected formats are:

- **Facts:**  
  Example: `Loves(John, Mary)` or `P`
  
- **Rules:**  
  Example: `Likes(x, IceCream) -> Happy(x)` or `P, Q -> R`

### Running the Scripts

#### Proof Tree Version

1. Open a terminal.
2. Run the script:
   python forward_chaining.py
3. When prompted, enter the path to your knowledge base file (e.g., `knowledge_base.txt`).
4. Enter your query (e.g., `V`).
5. The script will display whether the query is derivable and, if so, a proof tree showing the inference steps.

#### Rule Trace Version

1. Open a terminal.
2. Run the script:
   
   python forward_chaining_2.py
  
3. When prompted, enter the path to your knowledge base file (e.g., `knowledge_base_2.txt`).
4. Enter your query predicate (e.g., `Loves(Anna, Paul)`).
5. The script will display the initial facts, the rules applied, and the final derivation result.

## Examples

### Example 1: Rule Trace Version

#### Knowledge Base (`knowledge_base_2.txt`)
Loves(John, Mary)
Friend(John, Paul)
Friend(Mary, Paul)
Respects(Anna, John)
Respects(Anna, Paul)
Loves(Mary, x) -> Loves(John, x)
Loves(John, x) -> Likes(x, IceCream)
Loves(Anna, John) -> Loves(Anna, x)
Likes(x, IceCream) -> Happy(x)
Respects(x, y) -> Loves(x, y)

#### Execution
Enter the path to the input file: knowledge_base_2.txt
Enter the query predicate: Loves(Anna, Paul)

Initial Facts:
- Loves(John, Mary)
- Friend(John, Paul)
- Friend(Mary, Paul)
- Respects(Anna, John)
- Respects(Anna, Paul)
Rule Applied: Loves(John, x) -> Likes(Mary, IceCream)
Rule Applied: Likes(x, IceCream) -> Happy(Mary)
Rule Applied: Respects(x, y) -> Loves(Anna, John)
Rule Applied: Respects(x, y) -> Loves(Anna, Paul)

The query 'Loves(Anna, Paul)' is derivable (True).
Enter the query predicate or enter '0' to exit: 0

### Example 2: Proof Tree Version

#### Knowledge Base (`knowledge_base.txt`)
P
R
U
A
B
D
P -> Q
Q -> V
R -> S
U -> W
A, B -> C
C, D -> E
E -> J
P, R -> T
T, C -> L

#### Execution
Query ( Input From User): V
The query 'V' is derivable (True).

Proof tree:
V ↓
  Q ↓
    P

Other example:
Query ( Input From User): D
The query 'D' is not derivable (False).

## Requirements

- Python 3.6 or later.
- No additional libraries required.

## License

This project is open source. Feel free to modify and use it as needed.
```
