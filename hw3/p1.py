import copy 
from tabulate import tabulate
from fractions import Fraction
from itertools import permutations, combinations

def generate_probability_matrix(profile, alternatives):
    Q = [[0 for _ in range(len(alternatives.keys()))] for _ in range(len(alternatives.keys()))]
    pairs = list(combinations(alternatives.keys(),2))
    for ballot in profile:
        for pair in pairs:
            i, j = pair[0], pair[1]
            pos_i, pos_j = ballot.index(i), ballot.index(j) 
            if pos_i < pos_j:
                Q[alternatives[i]][alternatives[j]] = Q[alternatives[i]][alternatives[j]] + 1
            else:
                Q[alternatives[j]][alternatives[i]] = Q[alternatives[j]][alternatives[i]] + 1
    
    # For data storing purposes
    data_Q = copy.deepcopy(Q)

    # For display purposes
    for i in range(len(Q)):
        for j in range(len(Q[0])):
            Q[i][j] = str(Fraction(Q[i][j],len(profile)))
            data_Q[i][j] = data_Q[i][j] / len(profile)

    
    col_label = row_label = list(alternatives.keys())
    Q = [[row_label[i]] + row for i, row in enumerate(Q)]
    print(tabulate(Q, headers=[""] + col_label, tablefmt="grid"))

    return data_Q

def compute_winning_probabilities(probability_matrix, alternatives):
    
    def do(x, v, Q, candidates):
        # Base case
        if isinstance(v, list) and len(v) == 1 and v[0] == x:
            return 1
        elif isinstance(v, list) and len(v) == 1:
            return 0

        # Recursion steps
        l, r = v

        # Check if candidate is in left descendants or right descendants
        # This makes the left and right positioning relative to which candidate is being examined
        # ex. if computing probabilities for 'a' then 'b' is the right candidate 
        # ex. if computing probabilities for 'b' then 'a' is the right candidate (even though it is technically on the left in the tree)
        if x in descendants(l):
            g_x = do(x, l, Q, candidates) * sum(do(y, r, Q, candidates) * Q[candidates[x]][candidates[y]] for y in descendants(r))
        else:
            g_x = do(x, r, Q, candidates) * sum(do(y, l, Q, candidates) * Q[candidates[x]][candidates[y]] for y in descendants(l))

        return g_x
    
    def descendants(v):
        # Base case: Return singleton / leaf
        if len(v) == 1 and isinstance(v[0], str):
            return {v[0]}
        # Recursion steps: Return subtree recursively 
        elif len(v) == 2:
            return descendants(v[0]).union(descendants(v[1]))

    T = [[[['a'],['b']],[['c'],['d']]],[[['e'],['f']],[['g'],['h']]]]
    
    print("\n")
    result = {alternative : do(alternative, T, probability_matrix, alternatives) for alternative, _ in alternatives.items()}
    for alt, res in result.items():
        print(f"candidate {alt} has winning probability {res}")
    winner = [key for key, value in result.items() if value == max(result.values())].pop()
    print(f"\nTherefore the winning alternative is {winner} with probability {max(result.values())}")



if __name__ == "__main__":
    P_1 = ["b,a,c,h,g,f,e,d",
           "a,b,g,f,h,c,e,d",
           "h,e,b,f,a,g,c,d",
           "b,h,g,a,e,f,c,d",
           "b,f,d,a,g,c,h,e",
           "d,g,f,e,a,h,b,c",
           "e,c,f,h,b,a,g,d",
           "d,b,a,g,f,c,h,e",
           "b,h,f,g,e,a,c,d"]
    P_1 = [_.split(",") for _ in P_1]
    x = copy.deepcopy(P_1[0])
    x.sort()
    A = {x[_]: _ for _ in range(len(x))}
    Q = generate_probability_matrix(P_1, A)
    compute_winning_probabilities(Q, A)
