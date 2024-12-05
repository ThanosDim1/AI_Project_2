def read_kb(file_path):
    kb = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '->' in line:
                premises, conclusion = line.split('->')
                premises = [p.strip() for p in premises.split(',')]
                conclusion = conclusion.strip()
                if conclusion in kb:
                    kb[conclusion].append(premises)
                else:
                    kb[conclusion] = [premises]
            else:
                symbol = line.strip()
                if symbol in kb:
                    kb[symbol].append([])
                else:
                    kb[symbol] = [[]]
    return kb

def forward_chaining(kb, query):
    if query not in kb:
        return f"The type '{query}' is not found in the knowledge base."

    inferred = {sym: False for sym in kb}
    agenda = [sym for sym in kb if not any(kb[sym])]
    
    while agenda:
        p = agenda.pop(0)
        if not inferred[p]:
            inferred[p] = True
            for conclusion, clauses in kb.items():
                for clause in clauses:
                    if p in clause and all(inferred.get(sym, False) for sym in clause):
                        if not inferred[conclusion]:
                            agenda.append(conclusion)
    
    return f"The type '{query}' is {'true' if inferred.get(query, False) else 'false'} according to the knowledge base."

# Reading the knowledge base from the file
file_path = 'knowledge_base.txt'
kb = read_kb(file_path)

# Input the query type
query = input("Enter the type to be proven: ").strip()

# Perform forward chaining
result = forward_chaining(kb, query)
print(result)
