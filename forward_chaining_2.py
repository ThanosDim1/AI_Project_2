import os   # Import the os module to access file operations
import sys  # Import the sys module to access command-line arguments

def KBread():   # Read and parse predicates from a text file.
    """
    Read and parse predicates from a text file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        list: A list of parsed predicates.
    """
    try:
        file_path = input("Enter the path to the input file: ").strip()

        # Check if the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file at '{file_path}' does not exist.")   

        with open(file_path, 'r') as file:  # Open the file in read mode
            lines = file.readlines()        # Read all lines into a list
        predicates = []             # Initialize an empty list to store parsed predicates
        for line in lines:          # Iterate over each line
            line = line.strip()     # Remove leading/trailing whitespace
            if '->' in line:        # Rule
                premise, conclusion = line.split('->')  # Split the line into premise and conclusion
                predicates.append({         # Append the parsed rule to the list
                    'type': 'rule',         # Type of predicate (rule)
                    'if': parse(premise.strip()),       # Parse the premise (condition)
                    'then': parse(conclusion.strip())   # Parse the conclusion (fact)
                })
            elif line:  # Fact
                predicates.append({         # Append the parsed fact to the list
                    'type': 'fact',         # Type of predicate (fact)
                    'fact': parse(line)     # Parse the fact    
                })
        return predicates   # Return the list of parsed predicates
    except FileNotFoundError as e:  # Handle file not found error
        print(f"Error: {e}")  # Print the error message
        sys.exit(1)           # Exit the program
    except PermissionError:   # Handle permission error
        print("Error: You do not have permission to access this file.") # Print the error message
        sys.exit(1)           # Exit the program
    except Exception as e:    # Handle other exceptions
        print(f"An unexpected error occurred: {e}") # Print the error message
        sys.exit(1)           # Exit the program

def parse(predicate):         # Parse a predicate string like Loves(John,Mary) into a dictionary.
    """
    Parse a predicate string like Loves(John,Mary) into a dictionary.   

    Args:
        predicate (str): The predicate string, e.g., "Loves(John,Mary)"

    Returns:
        dict: Parsed predicate, e.g., {'predicate': 'Loves', 'args': ['John', 'Mary']}
    """
    name_start = predicate.index('(')   # Find the index of the opening parenthesis
    name_end = predicate.index(')')     # Find the index of the closing parenthesis
    name = predicate[:name_start]       # Extract the predicate name
    args = predicate[name_start+1 : name_end].split(',')                    # Extract the arguments and split them
    return {'predicate': name, 'args': [arg.strip() for arg in args]}       # Return the parsed predicate

def unify(predicate, fact):     # Attempt to unify a predicate with a fact.
    """
    Attempt to unify a predicate with a fact.

    Args:
        predicate (dict): The predicate with possible variables.
        fact (dict): The fact with concrete arguments.

    Returns:
        dict or None: A mapping of variables to values if unification succeeds, otherwise None.
    """
    if predicate['predicate'] != fact['predicate']: # Mismatch on the predicate name
        return None
    if len(predicate['args']) != len(fact['args']): # Mismatch on the number of arguments
        return None

    substitution = {}   # Initialize an empty substitution mapping
    for pred_arg, fact_arg in zip(predicate['args'], fact['args']):     # Iterate over the arguments
        if pred_arg.islower():     # Variable in the predicate argument (lowercase) 
            if pred_arg in substitution and substitution[pred_arg] != fact_arg:     # Variable already bound to a different value
                return None 
            substitution[pred_arg] = fact_arg       # Bind the variable to the value 
        elif pred_arg != fact_arg:                  # Mismatch on a constant
            return None

    return substitution     # Return the substitution mapping


def apply_substitution(predicate, substitution):    # Apply a substitution to a predicate.
    """
    Apply a substitution to a predicate.

    Args:
        predicate (dict): The predicate to modify.
        substitution (dict): The variable-to-value mapping.

    Returns:
        dict: The predicate with variables substituted.
    """
    return {
        'predicate': predicate['predicate'],        # Keep the predicate name
        'args': [substitution.get(arg, arg) for arg in predicate['args']]       # Substitute variables with values
    }


def forward_chaining(predicates, query):        # Perform forward chaining on a set of parsed predicates.
    """
    Perform forward chaining on a set of parsed predicates.

    Args:
        predicates (list): A list of parsed predicates.

    Returns:
        None: Prints facts and deduced facts.
    """
    facts = []      # Initialize an empty list to store facts
    rules = []      # Initialize an empty list to store rules

    # Separate facts and rules
    for pred in predicates:     # Iterate over the predicates
        if pred['type'] == 'fact':      # Fact
            facts.append(pred['fact'])  # Append the fact to the list
        elif pred['type'] == 'rule':    # Rule
            rules.append(pred)          # Append the rule to the list

    print("\nInitial Facts:")   # Print the initial facts
    for fact in facts:          # Iterate over the facts
        print(f"- {fact['predicate']}({', '.join(fact['args'])})")      # Print the fact

    newfact = True      # Initialize a flag to track new facts

    while newfact:      # Loop until no new facts are deduced
        newfact = False     # Reset the flag
        for rule in rules:  # Iterate over the rules
            premise, conclusion = rule['if'], rule['then']  # Extract the premise and conclusion

            # Check if the premise matches any current facts with unification
            for fact in facts:                          # Iterate over the facts
                substitution = unify(premise, fact)     # Attempt to unify the premise with the fact
                if substitution:                        # Unification successful
                    new_fact = apply_substitution(conclusion, substitution)     # Apply the substitution to the conclusion
                    if new_fact not in facts:           # Check if the new fact is not already deduced
                        print(f"Rule Applied: {premise['predicate']}({', '.join(premise['args'])}) -> {new_fact['predicate']}({', '.join(new_fact['args'])})") # Print the rule application
                        facts.append(new_fact)          # Append the new fact to the list
                        newfact = True                  # Set the flag to True to continue the loop 

    for fact in facts:      # Iterate over the facts
        if query == f"{fact['predicate']}({', '.join(fact['args'])})":      # Check if the query is derivable
            print(f"\nThe query '{query}' is derivable (True).")            # Print the result
            return 
    return print(f"\nThe query '{query}' is not derivable (False).")        # Print the result

def main():     # Main function to read predicates and perform forward chaining.

    # Read predicates from the file
    predicates = KBread()       # Read and parse predicates from a text file

    query = input("Enter the query predicate: ").strip()   # Get the query predicate

    while query != "0":    # Loop until the user enters '0' to exit
        # Perform forward chaining
        forward_chaining(predicates, query)    # Perform forward chaining on the parsed predicates and query
        query = input("Enter the query predicate or enter '0' to exit: ").strip()   # Get the next query predicate       
    return

if __name__ == "__main__":  
    main()