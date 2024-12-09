def forward_chaining_with_proof(facts, rules, query):
    # Initialize known facts and proof tree
    known_facts = set(facts)
    proof_tree = {fact: [] for fact in facts}
    changed = True

    while changed:
        changed = False
        for rule in rules:
            premises = rule[:-1]
            conclusion = rule[-1]
            if conclusion not in known_facts and all(premise in known_facts for premise in premises):
                known_facts.add(conclusion)
                proof_tree[conclusion] = premises
                changed = True

    # Build proof for the query
    def build_proof_tree(fact, tree):
        if fact not in tree or not tree[fact]:
            return fact  # Base case: fact is an initial fact
        return {fact: [build_proof_tree(premise, tree) for premise in tree[fact]]}

    if query in known_facts:
        proof = build_proof_tree(query, proof_tree)
        return True, proof
    else:
        return False, None


# Read data from file
file_path = "knowledge_base.txt"
with open(file_path, "r") as file:
    lines = file.read().splitlines()

# Parse the facts and rules
facts = set()
rules = []

for line in lines:
    if "->" in line:
        premises, conclusion = line.split("->")
        rules.append([premise.strip() for premise in premises.split(",")] + [conclusion.strip()])
    else:
        facts.add(line.strip())

# Test the forward chaining algorithm
query = input("Enter query: ").strip()
result, proof = forward_chaining_with_proof(facts, rules, query)

if result:
    print("True")
    print("Proof tree:", proof)
else:
    print("False")
