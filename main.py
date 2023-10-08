import random
import string

def find_highest_index(lst):
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_index

def add_node(node_type, node_data):
    if node_type == 'input' or node_type == 'middle':
        return [0, {item: random.uniform(0, 0) for item in node_data}]
    elif node_type == 'output':
        return node_data

def generate_random_rule():
    operators = ['<', '>']
    operator = random.choice(operators)
    if True:
        return operator
    else:
        return '<'

def test_rule(operator, num1, num2):
    if operator == '<':
        return num1 < num2
    elif operator == '>':
        return num1 > num2

def mutate_weights(weights, amount):
    mutated_weights = {}
    for key, value in weights.items():
        mutated_weights[key] = (value + random.uniform(-amount, amount))
##        if mutated_weights[key] < -2:
##            mutated_weights[key] = -2
##        if mutated_weights[key] > 2:
##            mutated_weights[key] = 2
    return mutated_weights

def mutate(brain, mutation_amount):
    ins = brain[0]
    mids = brain[1]
    outs = brain[2]

    for key, value in ins.items():
        ins[key][1] = mutate_weights(ins[key][1], mutation_amount)
    
    for i in range(len(mids)):
        for key, value in mids[i].items():
            mids[i][key][1] = mutate_weights(mids[i][key][1], mutation_amount)
    
    return [ins, mids, outs]

def wxi(node_id, connection, lst):
    return lst[node_id][0] * lst[node_id][1][connection]

def setup_nodes(input_amt, hidden_amt, middle_amt, output_amt):
    ins = {}
    mids = []
    outs = {}

    for i in range(input_amt):
        ins[str(i + 1)] = add_node('input', list(string.ascii_lowercase[:middle_amt]))

    for i in range(hidden_amt):
        mids.append({})
        for j in range(middle_amt):
            if i == (hidden_amt - 1):
                mids[i][list(string.ascii_lowercase)[j]] = add_node('middle', list(string.ascii_lowercase[:output_amt]))
            else:
                mids[i][list(string.ascii_lowercase)[j]] = add_node('middle', list(string.ascii_lowercase[:middle_amt]))

    for i in range(output_amt):
        outs[list(string.ascii_lowercase)[i]] = 0
    
    return [ins, mids, outs]

def run_ai(brain, inputs, example):
    ins = brain[0]
    mids = brain[1]
    outs = brain[2]
    
    for i in range(len(ins)):
        ins[str(i + 1)][0] = inputs[i]

    for i in range(len(mids)):
        for key, value in mids[i].items():
            mids[i][key][0] = 0
            if i == 0:
                for inskey, insvalue in ins.items():
                    mids[i][key][0] = mids[i][key][0] + wxi(inskey, key, ins)
            else:
                for midskey, midsvalue in mids[i - 1].items():
                    mids[i][key][0] = mids[i][key][0] + wxi(midskey, key, mids[i - 1])

    for key, value in outs.items():
        outs[key] = 0
        for midkey, midvalue in mids[len(mids) - 1].items():
            outs[key] += wxi(midkey, key, mids[len(mids) - 1])

    ans = None

    if outs['a'] > outs['b']:
        ans = True

    if outs['b'] > outs['a']:
        ans = False
    
    if example == 'before':
        if test_rule(rule, inputs[0], inputs[1]) == ans:
            return True
        else:
            return False
    elif example == 'after':
        return ans

rule = generate_random_rule()

print(rule)
print()

amt_of_brains = 50

brains = []
for i in range(amt_of_brains):
    brains.append(setup_nodes(2, 1, 4, 2)) # Neural Network Node Amount Settings

brain_performances = [0] * len(brains)

parts = 200

train_amount = 500 * parts


very_best_brain = []
vbb_score = 0

mutation_amount = 1

for part in range(parts):
    for i in range(int(train_amount / parts)):
        for current_brain in range(len(brains)):
            if run_ai(brains[current_brain], [random.uniform(-10.00, 10.00), random.uniform(-10.00, 10.00)], 'before'):
                brain_performances[current_brain] += 1
            else:
                brain_performances[current_brain] -= 1

    best_brain_index = find_highest_index(brain_performances)

    if brain_performances[best_brain_index] > vbb_score:
        vbb_score = brain_performances[best_brain_index]
        very_best_brain = brains[best_brain_index]

    accuracy_percent = (((brain_performances[best_brain_index] / (train_amount / parts)) * 100) + 100) / 2
    
    if True:
        print('Best Run Accuracy: ' + str(accuracy_percent) + '%')

    if accuracy_percent <= 10:
        mutation_amount = 1
    elif accuracy_percent <= 20:
        mutation_amount = 0.35
    elif accuracy_percent <= 50:
        mutation_amount = 0.1
    elif accuracy_percent <= 75:
        mutation_amount = 0.05
    elif accuracy_percent <= 90:
        mutation_amount = 0.01
    elif accuracy_percent <= 95:
        mutation_amount = 0.005
    elif accuracy_percent <= 98:
        mutation_amount = 0.001
    elif accuracy_percent == 100:
        mutation_amount = 0
    
    if part != (parts - 1):
        for j in range(amt_of_brains):
            brain_performances[j] = 0
            if j != best_brain_index:
                brains[j] = mutate(brains[best_brain_index], mutation_amount)

print()
print('Very Best Brain Score: ' + str(((vbb_score / (train_amount / parts) * 100) + 100) / 2) + '%')
print()
print('Very Best Brain: ' + str(very_best_brain))
print(f'\n\n\nThe Rule Is \'{rule}\'.\n')

while True:
    number_1 = float(input('Number Input 1: '))
    number_2 = float(input('Number Input 2: '))

    print(run_ai(very_best_brain, [number_1, number_2], 'after'))
