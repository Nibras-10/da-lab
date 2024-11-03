from itertools import chain, combinations

def load_data(file_path):
    transactions = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            parts = line.strip().split(',')
            tid = parts[0]  # Transaction ID
            items = parts[1:]  # Remaining parts are items
            transaction = set(items)
            transactions.append(transaction)
    return transactions


def get_unique_items(data):
    unique_items = set()
    for transaction in data:
        for item in transaction:
            unique_items.add(frozenset([item]))
    return unique_items

def support_count(data, itemset):
    count = 0
    for transaction in data:
        if itemset.issubset(transaction):
            count += 1
    return count

def generate_candidate_itemsets(prev_itemsets, k):
    candidates = set()
    prev_itemsets_list = list(prev_itemsets)
    for i in range(len(prev_itemsets_list)):
        for j in range(i + 1, len(prev_itemsets_list)):
            union = prev_itemsets_list[i] | prev_itemsets_list[j]
            if len(union) == k:
                candidates.add(union)
    return candidates

def apriori(data, min_support):
    unique_items = get_unique_items(data)
    frequent_itemsets = {}
    k = 1
    while True:
        if k == 1:
            candidate_itemsets = unique_items
        else:
            candidate_itemsets = generate_candidate_itemsets(prev_itemsets, k)
        prev_itemsets = candidate_itemsets.copy()
        frequent_itemsets_k = {}
        for itemset in candidate_itemsets:
            support = support_count(data, itemset)
            if support >= min_support:
                frequent_itemsets_k[itemset] = support
        if not frequent_itemsets_k:
            break
        frequent_itemsets.update(frequent_itemsets_k)
        k += 1
    return frequent_itemsets

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))

def generate_rules(data, frequent_itemset, support, min_confidence):
    rules = []
    for antecedent in map(set, powerset(frequent_itemset)):
        if antecedent and antecedent != frequent_itemset:
            consequent = frequent_itemset - antecedent
            if support_count(data, antecedent) > 0:
                confidence = support / support_count(data, antecedent)
                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, confidence))
    return rules

min_support = 2
min_confidence = 0.75
data = load_data("transactions2.csv")
transactions = data  # Use transactions directly
frequent_itemsets = apriori(transactions, min_support)

print("Frequent Itemsets and their Support Counts:")
for itemset, support in frequent_itemsets.items():
    print(f"{set(itemset)}: {support}")

print("\nAssociation Rules:")
for itemset, support in frequent_itemsets.items():
    rules = generate_rules(transactions, itemset, support, min_confidence)
    for rule in rules:
        antecedent, consequent, confidence = rule
        print(f"{set(antecedent)} => {set(consequent)} (Confidence: {confidence:.2f})")
