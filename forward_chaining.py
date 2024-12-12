import os
import sys

# Build proof for the query
def build_proof_tree(fact, tree):
    if fact not in tree or not tree[fact]:
        return fact  # Base case: fact is an initial fact
    return {fact: [build_proof_tree(premise, tree) for premise in tree[fact]]}

def pretty_print_proof(proof, indent=0):
    """Recursively print the proof tree in a user-friendly format."""
    if isinstance(proof, dict):
        for fact, premises in proof.items():
            print("  " * indent + f"{fact} ↓")
            for premise in premises:
                pretty_print_proof(premise, indent + 1)
    else:
        print("  " * indent + f"{proof}")

def KBread():
    try:
        file_path = input("Enter the path to the input file: ").strip()

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file at '{file_path}' does not exist.")

        with open(file_path, "r") as file:
            lines = file.read().splitlines()
        rules = []
        facts = set()
        for line in lines:
            line = line.strip()
            if "->" in line:
                premises, conclusion = line.split("->")
                rules.append([premise.strip() for premise in premises.split(",")] + [conclusion.strip()])
            else:
                facts.add(line)  # Add the positive fact to facts
        return facts, rules
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except PermissionError:
        print("Error: You do not have permission to access this file.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def forward_chaining(facts, rules, query):
    # Initialize known facts, negative facts, and proof tree
    known_facts = set(facts) # Known facts

    proof_tree = {fact: [] for fact in facts} # Proof tree
    new_fact = True # Flag to indicate if any new fact is inferred in the current iteration

    # Forward chaining process
    while new_fact:
        new_fact = False
        # Iterate over each rule
        for rule in rules:
            premises, conclusion = rule[:-1], rule[-1]

            # Check if any premise is a negative fact (i.e., a fact is negated)
            if conclusion not in known_facts:
                known_facts.add(conclusion) # Add the conclusion to known facts
                proof_tree[conclusion] = premises # Add the premises to the proof tree
                new_fact = True # Set the flag to True to continue the process

    # After forward chaining, check if the query is a fact or its negation
    if query in known_facts:
        return True, build_proof_tree(query, proof_tree)
    else:
        return False, None

def main():

    # Load the knowledge base
    facts, rules = KBread()

    # User input for the query
    query = input("Enter the query you want to check (e.g., F): ").strip()

    while query != "0":
        # Test the forward chaining algorithm
        result, proof = forward_chaining(facts, rules, query)

        if result:
            print(f"\nThe query '{query}' is derivable (True).")
            print("\nProof tree:")
            pretty_print_proof(proof)
        else:
            print(f"\nThe query '{query}' is not derivable (False).")

        query = input("\nEnter the query you want to check (e.g., F) or enter '0' to exit: ").strip()
    return

if __name__ == "__main__":
    main()