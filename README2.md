# Forward Chaining with propositional predicate logic

## Overview

This project implements a **Forward Chaining with propositional predicate logic**. It uses a knowledge base of facts and rules to determine if a given query is true or false. The system employs the forward chaining algorithm and provides the facts, the applied rules and the result of your query.

---

## Features

- **Forward Chaining Algorithm**: Derives new facts iteratively based on the rules.
- **Facts and applied rules Generation**: Explains how the query is derived or why it is not.
- **Customizable Knowledge Base**: Add facts and rules easily via a text file.
- **Interactive Queries**: Input queries dynamically and get instant results.

---

## Files

- **`knowledge_base_2.txt`**: Contains facts, negative facts, and rules.
- **`forward_chaining_2.py`**: The Python script implementing the inference system.

---

## How to Use

1. **Set Up the Knowledge Base**:
   - Open `knowledge_base_2.txt`.
   - Add facts and rules in the following format:
     - **Facts**: `Friend(John, Paul)`
     - **Rules**: `Likes(x, IceCream) -> Happy(x)`

2. **Run the Script**:
   - Execute the Python script:
     ```bash
     python forward_chaining_2.py
     ```

3. **Input a Query**:
   - When prompted, type the query to check (e.g., `Loves(Anna, Paul)`).

4. **View the Results**:
   - The script will indicate if the query is true or false and the facts, rules that were used for the result.

---