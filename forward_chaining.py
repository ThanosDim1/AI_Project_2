def forward_chaining_with_proof(facts,negative_facts, rules, query):
    # Initialize known facts, negative facts, and proof tree
    known_facts = set(facts)
    negative_facts = set(negative_facts)
    proof_tree = {fact: [] for fact in facts}
    changed = True

    while changed:
        changed = False
        for rule in rules:
            premises = rule[:-1]
            conclusion = rule[-1]
            
            # Check if any premise is a negative fact (i.e., a fact is negated)
            if conclusion not in known_facts and all(
                (premise in known_facts or premise not in negative_facts) for premise in premises):
                known_facts.add(conclusion)
                proof_tree[conclusion] = premises
                changed = True

    # After forward chaining, check if the query is a fact or its negation
    if query in known_facts:
        proof = build_proof_tree(query, proof_tree)
        return True, proof
    elif f"!{query}" in negative_facts:
        proof = build_proof_tree(f"!{query}", proof_tree)
        return False, proof
    else:
        return False, None



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

# Read data from file
file_path = "knowledge_base.txt"
with open(file_path, "r") as file:
    lines = file.read().splitlines()

# Parse the facts and rules
facts = set()
rules = []

facts = set()
negative_facts = set()
for line in lines:
    line = line.strip()
    if "->" in line:
        premises, conclusion = line.split("->")
        rules.append([premise.strip() for premise in premises.split(",")] + [conclusion.strip()])
    else:
        # Handle negative facts
        if line.startswith("!"):
            negative_facts.add(line[1:].strip())  # Add the fact without '!' to negative_facts
        else:
            facts.add(line)  # Add the positive fact to facts

# User input for the query
query = input("Enter the query you want to check (e.g., F): ").strip()

# Test the forward chaining algorithm
result, proof = forward_chaining_with_proof(facts, negative_facts, rules, query)

if result:
    print(f"\nThe query '{query}' is derivable (True).")
    print("\nProof tree:")
    pretty_print_proof(proof)
else:
    print(f"\nThe query '{query}' is not derivable (False).")
