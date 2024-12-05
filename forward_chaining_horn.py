def read_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    facts = set()
    rules = []
    for line in lines:
        line = line.strip()
        if '->' in line:
            premise, conclusion = line.split('->')
            premise = premise.strip().split(', ')
            conclusion = conclusion.strip()
            rules.append((premise, conclusion))
        else:
            facts.add(line)
    return facts, rules


def forward_chaining(facts, rules, query):
    inferred = set(facts)
    new_inferences = True
    
    while new_inferences:
        new_inferences = False
        for premise, conclusion in rules:
            if conclusion not in inferred:
                if all(p in inferred for p in premise):
                    inferred.add(conclusion)
                    new_inferences = True
                    if conclusion == query:
                        return True
    return query in inferred


def main():
    file_path = 'knowledge_base_horn.txt'
    facts, rules = read_knowledge_base(file_path)
    
    query = input("Εισάγετε τον προς απόδειξη τύπο: ").strip()
    
    if forward_chaining(facts, rules, query):
        print(f"Αληθές: Το {query} αποδείχθηκε από τη βάση γνώσεων.")
    else:
        print(f"Ψευδές: Το {query} δεν αποδείχθηκε από τη βάση γνώσεων.")


if __name__ == "__main__":
    main()
