import os   # Import the os module
import sys  # Import the sys module

# Build proof for the query
def build_proof_tree(fact, tree):               # Build a proof tree for a given fact. 
    if fact not in tree or not tree[fact]:      # If the fact is not in the tree or has no premises
        return fact  # Base case: fact is an initial fact   
    return {fact: [build_proof_tree(premise, tree) for premise in tree[fact]]}  # Recursive case: build the proof tree

def print_proof_tree(proof_tree, space=0):        # Recursively print the proof tree in a user-friendly format.

    if isinstance(proof_tree, dict):              # If the proof is a dictionary
        for fact, premises in proof_tree.items():    # Iterate over the fact and premises
            print("  " * space + f"{fact} ↓")   # Print the fact
            for premise in premises:         # Iterate over the premises
                print_proof_tree(premise, space + 1)  # Recursively print the premises
    else:                                   # If the proof is a fact
        print("  " * space + f"{proof_tree}")    # Print the fact

def KBread():   # Read and parse predicates from a text file.
    try:        # Try block to handle exceptions
        file_path = input("Enter the path to the input file: ").strip() # Get the file path from the user input

        if not os.path.isfile(file_path):       # Check if the file exists
            raise FileNotFoundError(f"The file at '{file_path}' does not exist.")   # Raise a FileNotFoundError

        with open(file_path, "r") as file:      # Open the file in read mode
            lines = file.read().splitlines()    # Read the lines and split them
        rules = []           # Initialize an empty list for rules
        facts = set()        # Initialize an empty set for facts
        for line in lines:   # Iterate over the lines
            line = line.strip() # Remove leading/trailing whitespace
            if "->" in line:    # Rule
                premises, conclusion = line.split("->") # Split the line into premises and conclusion
                rules.append([premise.strip() for premise in premises.split(",")] + [conclusion.strip()])   # Append the rule to the list
            else:               # Fact
                facts.add(line) # Add the positive fact to facts
        return facts, rules     # Return the facts and rules
    except FileNotFoundError as e:  # Handle file not found error
        print(f"Error: {e}")        # Print the error message
        sys.exit(1)                 # Exit the program
    except PermissionError:         # Handle permission error
        print("Error: You do not have permission to access this file.") # Print the error message
        sys.exit(1)                 # Exit the program
    except Exception as e:          # Handle other exceptions
        print(f"An unexpected error occurred: {e}") # Print the error message
        sys.exit(1)                 # Exit the program

def forward_chaining(agenda, rules, query):     # Implement the forward chaining algorithm.
    # Initialize known facts, negative facts, and proof tree
    agenda = set(agenda) # Known facts

    proof_tree = {fact: [] for fact in agenda} # Proof tree
    inferred = True # Flag to indicate if any new fact is inferred in the current iteration

    # Forward chaining process
    while inferred: # Continue until no new fact is inferred. Inferred means that the fact is added to the agenda. 
        inferred = False    # Reset the flag to False
        for rule in rules:                              # Iterate over each rule
            premises, conclusion = rule[:-1], rule[-1]  # Split the rule into premises and conclusion

            # Check if any premise is a negative fact (i.e., a fact is negated)
            if conclusion not in agenda:          # If the conclusion is not in the agenda
                agenda.add(conclusion)            # Add the conclusion to known facts
                proof_tree[conclusion] = premises # Add the premises to the proof tree
                inferred = True                   # Set the flag to True to continue the process

    # After forward chaining, check if the query is a fact or its negation
    if query in agenda:
        return True, build_proof_tree(query, proof_tree)        # Return True and the proof tree
    else:
        return False, None                                      # Return False and None

def main():     # Main function to test the forward chaining algorithm.

    # Read the facts and rules from the input file
    facts, rules = KBread()     

    # User input for the query
    query = input("Enter the query you want to check (e.g., F): ").strip()

    while query != "0":
        # Test the forward chaining algorithm
        result, proof = forward_chaining(facts, rules, query)

        if result:
            print(f"\nThe query '{query}' is derivable (True).")    # Print the result
            print("\nProof tree:")                                  # Print the proof tree header
            print_proof_tree(proof)  # Print the proof tree
        else:
            print(f"\nThe query '{query}' is not derivable (False).")   # Print the result

        query = input("\nEnter the query you want to check (e.g., F) or enter '0' to exit: ").strip() # Get the next query from the user input 
    return

if __name__ == "__main__":
    main()