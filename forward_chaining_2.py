import os
import sys

def KBread():
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

        with open(file_path, 'r') as file:
            lines = file.readlines()
        predicates = []
        for line in lines:
            line = line.strip()
            if '->' in line:
                premise, conclusion = line.split('->')
                predicates.append({
                    'type': 'rule',
                    'if': parse(premise.strip()),
                    'then': parse(conclusion.strip())
                })
            elif line:
                predicates.append({
                    'type': 'fact',
                    'fact': parse(line)
                })
        return predicates
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except PermissionError:
        print("Error: You do not have permission to access this file.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def parse(predicate):
    """
    Parse a predicate string like Loves(John,Mary) into a dictionary.

    Args:
        predicate (str): The predicate string, e.g., "Loves(John,Mary)"

    Returns:
        dict: Parsed predicate, e.g., {'predicate': 'Loves', 'args': ['John', 'Mary']}
    """
    name_start = predicate.index('(')
    name_end = predicate.index(')')
    name = predicate[:name_start]
    args = predicate[name_start+1 : name_end].split(',')
    return {'predicate': name, 'args': [arg.strip() for arg in args]}

def unify(predicate, fact):
    """
    Attempt to unify a predicate with a fact.

    Args:
        predicate (dict): The predicate with possible variables.
        fact (dict): The fact with concrete arguments.

    Returns:
        dict or None: A mapping of variables to values if unification succeeds, otherwise None.
    """
    if predicate['predicate'] != fact['predicate']:
        return None
    if len(predicate['args']) != len(fact['args']):
        return None

    substitution = {}
    for pred_arg, fact_arg in zip(predicate['args'], fact['args']):
        if pred_arg.islower():  # A variable (e.g., x, y)
            if pred_arg in substitution and substitution[pred_arg] != fact_arg:
                return None
            substitution[pred_arg] = fact_arg
        elif pred_arg != fact_arg:  # Mismatch on a constant
            return None

    return substitution


def apply_substitution(predicate, substitution):
    """
    Apply a substitution to a predicate.

    Args:
        predicate (dict): The predicate to modify.
        substitution (dict): The variable-to-value mapping.

    Returns:
        dict: The predicate with variables substituted.
    """
    return {
        'predicate': predicate['predicate'],
        'args': [substitution.get(arg, arg) for arg in predicate['args']]
    }


def forward_chaining(predicates, query):
    """
    Perform forward chaining on a set of parsed predicates.

    Args:
        predicates (list): A list of parsed predicates.

    Returns:
        None: Prints facts and deduced facts.
    """
    facts = []
    rules = []

    # Separate facts and rules
    for pred in predicates:
        if pred['type'] == 'fact':
            facts.append(pred['fact'])
        elif pred['type'] == 'rule':
            rules.append(pred)

    print("\nInitial Facts:")
    for fact in facts:
        print(f"- {fact['predicate']}({', '.join(fact['args'])})")

    newfact = True

    while newfact:
        newfact = False
        for rule in rules:
            premise, conclusion = rule['if'], rule['then']

            # Check if the premise matches any current facts with unification
            for fact in facts:
                substitution = unify(premise, fact)
                if substitution:
                    new_fact = apply_substitution(conclusion, substitution)
                    if new_fact not in facts:
                        print(f"Rule Applied: {premise['predicate']}({', '.join(premise['args'])}) -> {new_fact['predicate']}({', '.join(new_fact['args'])})")
                        facts.append(new_fact)
                        newfact = True

    for fact in facts:
        if query == f"{fact['predicate']}({', '.join(fact['args'])})":
            print(f"\nThe query '{query}' is derivable (True).")
            return
    return print(f"\nThe query '{query}' is not derivable (False).")

def main():

    # Read predicates from the file
    predicates = KBread()

    query = input("Enter the query predicate: ").strip()

    while query != "0":
        # Perform forward chaining
        forward_chaining(predicates, query)
        query = input("Enter the query predicate or enter '0' to exit: ").strip()
    return

if __name__ == "__main__":
    main()