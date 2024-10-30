from ..hw1.p1 import voting_rules

# if __name__ == "__main__":
#     voting_profile = {
#         "v1" : ["a", "c", "b", "f", "e", "d"],
#         "v2" : ["b", "a", "d", "f", "c", "e"],
#         "v3" : ["c", "f", "e", "b", "d", "a"],
#         "v4" : ["d", "b", "f", "c", "a", "e"],
#         "v5" : ["e", "f", "a", "c", "b", "d"]
#     }

#     alternatives = ("a", "b", "c", "d", "e")

#     load_rule = voting_rules(voting_profile, alternatives)

#     copeland_winner = load_rule.copeland_winner()
#     print("Copeland winner: {}" .format(copeland_winner))