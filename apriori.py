from itertools import combinations

min_sup=2
min_confidence=0.75

transactions=[]
file_path='transactions2.csv'
with open(file_path,'r')as file:
    next(file)
    for line in file:
        items = line.strip().split(',')[1:]
        transactions.append(items)

item_counts={}
for transaction in transactions:
    for item in transaction:
        if item in item_counts:
            item_counts[item]+=1
        else:
            item_counts[item]=1

for item,count in item_counts.items():
    if count>=min_sup:
        print(f'{item}=>{count}')
print()

pair_counts={}
for transaction in transactions:
    pairs=list(combinations(transaction,2))
    for pair in pairs:
        pair=tuple(sorted(pair))
        if pair in pair_counts:
            pair_counts[pair]+=1
        else:
            pair_counts[pair]=1

for pair,count in pair_counts.items():
    if count>=min_sup:
        print(f"{{{pair}}}=>{{{count}}}")

triple_counts={}
for transaction in transactions:
    triples=list(combinations(transaction,3))
    for triple in triples:
        triple=tuple(sorted(triple))
        if triple in triple_counts:
            triple_counts[triple]+=1
        else:
            triple_counts[triple]=1

for i,c in triple_counts.items():
    if c>=min_sup:
        print(f"{i}=>{c}")   

for pair,support in pair_counts.items():
    if support>=min_sup:
        item1,item2=pair

        conf=support/item_counts[item1]
        if conf>=min_confidence:
            print(f"{item1}=>{item2} confidence:{conf:.2f}")
        
        conf=support/item_counts[item2]
        if conf>=min_confidence:
            print(f"{item2}=>{item1} confidence:{conf:.2f}")

for triple,support in triple_counts.items():
    if support>=min_sup:
        for i in range(3):
            item=list(triple)
            consequent=item.pop(i)
            antecedent=tuple(sorted(item))

            if antecedent in pair_counts:
                conf=support/pair_counts[antecedent]
                if conf>=min_confidence:
                    print(f'{{{', '.join(antecedent)}}} => {{{consequent}}} confidence:{conf:.2f}')

            conf2=support/item_counts[consequent]
            if conf2>=min_confidence:
                print(f"{{{consequent}}} => {{{', '.join(antecedent)}}} confidence:{conf2:.2f}")
