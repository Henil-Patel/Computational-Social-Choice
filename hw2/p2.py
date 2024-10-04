import itertools
from tabulate import tabulate
def kemeny_winner(voting_profile: dict, alternatives: tuple) -> set:
    disagreements = lambda x, y: sum(map (lambda pair: (x.index(pair[0]) < x.index(pair[1])) != (y.index(pair[0]) < y.index(pair[1])), all_pairs))
    all_linear_orderings = tuple(itertools.permutations(alternatives))
    all_pairs = tuple(itertools.combinations(alternatives, 2))
    ballots = tuple(voting_profile.values())
    counts = {}
    for ordering in all_linear_orderings:
        count = 0
        for ballot in ballots:
            # print(f"Comparing {ballot} with {ordering}")
            count = count + disagreements(ordering, ballot)
            counts.update({ordering: count})
    print("\n")
    counts = dict(sorted(counts.items(), key=lambda counts: counts[1]))
    print(tabulate([(k, v) for k,v in counts.items()], headers=["ordering", "distance"], tablefmt="grid"))
    return {k[0] for k,v in counts.items() if counts[k] == min(counts.values())}   


if __name__ == "__main__":
    voting_profile = {
        "v1" : ("a", "b", "c"),
        "v2" : ("a", "c", "b"),
        "v3" : ("b", "a", "c"),
        "v4" : ("b", "c", "a")
    }

    alternatives = ("a", "b", "c")

    winner = kemeny_winner(voting_profile, alternatives)
    print("\n----------------------------------------\n")
    print(f"Kemeny winners are: {winner}\n")