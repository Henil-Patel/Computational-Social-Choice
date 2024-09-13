import random 
import functools
import itertools

class voting_rules:

    def __init__(self, profile: dict, alternatives: tuple):
        '''
            Initialize class
        '''
        self.profile = profile
        self.NUM_VOTERS = len(self.profile.keys())
        self.alternatives = alternatives

    def plurality(self) -> str:
        '''
            This implements the plurality voting rule and returns the winner
        '''
        counts = utils.count_first_choice(self.profile)
        return utils.select_winner(counts)
    
    def single_transferable_vote(self) -> str: 
        '''
            This implements the STV voting rule with a tie breaking rule to determine loser
        '''           
        num_voters = self.NUM_VOTERS
        upper_echelon = self.profile
        while True:
            counts = utils.count_first_choice(upper_echelon)
            if utils.got_majority(counts, num_voters) == True or len(counts.keys()) == 2:
                return utils.select_winner(counts)
            lowest = utils.get_lowest_candidate(counts)
            if len(lowest) > 1:
                lower_echelon = utils.update_profile(lowest, upper_echelon, eliminate=False)
                lowest = utils.tie_breaker(lowest, lower_echelon, num_voters)
            upper_echelon = utils.update_profile(lowest, upper_echelon, eliminate = True)
    
    def borda_count(self) -> str:
        '''
            This implements the Borda count rule
        '''
        score = {alternatives : 0 for alternatives in self.alternatives}
        for _, preferences in self.profile.items():
            score = utils.map_alternative_to_score(preferences, score)
            print(score)
        return utils.select_winner(score)
    
    def condorcet_winner(self) -> str:
        '''
            This does all pair wise comparisons to determine if an alternative is preferred to ALL other alternatives
        '''
        all_pairs = {pair: 0 for pair in itertools.combinations(self.alternatives,2)}
        mutable_alternatives = set(self.alternatives)
        for _, preference in self.profile.items():
            all_pairs = utils.get_pairwise_score(all_pairs, preference)
        
        blacklisted_candidates = set()
        for pair, score in all_pairs.items():
            if score < int(self.NUM_VOTERS/2) + 1 or pair[0] in blacklisted_candidates:
                blacklisted_candidates.add(pair[0])
                continue

        remaining_candidates = mutable_alternatives.difference(blacklisted_candidates)            
        if len(remaining_candidates) == 1:
            return remaining_candidates.pop()  
        else:
            print("no clear condorcet winner")
            return remaining_candidates
        
    def copeland_winner(self) -> str:
        '''
            This implements Copeland's voting rule 
        '''
        all_pairs = {pair: 0 for pair in itertools.combinations(self.alternatives, 2)}
        for _, preference in self.profile.items():
            all_pairs = utils.get_pairwise_score(all_pairs, preference)
        initial = {self.alternatives[i]: i for i in range(len(self.alternatives))}
        matrix = utils.generate_matrix(all_pairs, set(self.alternatives), initial, self.NUM_VOTERS)
        row_agg, col_agg = utils.aggregate_matrix(matrix)
        diff = dict(map(lambda x, y, z: (z, x - y), row_agg, col_agg, self.alternatives))
        return utils.select_winner(diff)

class utils:

    def count_first_choice(profile: dict) -> dict:
        counts = {}
        for _, preference in profile.items():
            first_choice = preference[0]
            if first_choice in counts.keys():
                counts[first_choice] += 1
            else:
                counts[first_choice] = 1
        return counts 

    def get_lowest_candidate(counts: dict) -> str:
        lowest_candidates = {key for key in counts if counts.get(key) == min(counts.values())}
        if len(lowest_candidates) > 1:
            return lowest_candidates
        else:
            return lowest_candidates.pop()
    
    def got_majority(counts: dict, num_voters: int) -> bool:
        if max(counts.values()) > int(num_voters/2) + 1:
            return True
        else:
            return False
        
    def update_profile(lowest: set, profile: dict, eliminate: bool) -> dict:
        new_profile = {}
        for voter, preference in profile.items():
            if eliminate:
                new_preference = list(filter(lambda x: x != lowest, preference))
            else:
                new_preference = list(filter(lambda x: x in lowest, preference))
            new_profile[voter] = new_preference
        return new_profile
    
    def select_winner(counts: dict) -> str:
        return {key for key in counts if counts.get(key) == max(counts.values())}.pop()

    def map_alternative_to_score(preference: list, score: dict) -> dict:
        for alternative, _ in score.items():
            score[alternative] = score[alternative] + ((len(preference) - 1) - preference.index(alternative))
        return score
        
    def tie_breaker(lowest: set, profile: dict, num_voters: int) -> str:
        # Top cycle - but remove lowest scoring candidate
        lowest = sorted(lowest)
        position = {lowest[i]: i for i in range(len(lowest))}
        # print(f"identified {position}")
        while True:
            pairs = {pair: 0 for pair in itertools.combinations(lowest, 2)}
            for _, preference in profile.items():
                # print(pairs, preference)
                pairs = utils.get_pairwise_score(pairs, preference)

            mat = utils.generate_matrix(pairs, lowest, position, num_voters)
            # print(mat)
            score = [sum(row) for row in mat]
            # print(score)
            lowest = {key for key in position.keys() if position[key] == score.index(min(score))}
            if len(lowest) == 1:
                return lowest.pop()
            else:
                # Choose randomly otherwise
                return random.choice(lowest)

    def get_pairwise_score(pairs: dict, preference: list) -> dict:
        for pair, _ in pairs.items():
            if (preference.index(pair[0]) > preference.index(pair[1])):
                offset = 0
            else:
                offset = 1
            pairs[pair] = pairs[pair] + offset 
        return pairs
    
    def generate_matrix(pairs: dict, lowest: set, position: dict, num_voters: int) -> list:

        matrix = [[0 for _ in range(len(lowest))] for _ in range(len(lowest))]
        for pair, score in pairs.items():
            if score >= int(num_voters/2) + 1:
                matrix[position.get(pair[0])][position.get(pair[1])], matrix[position.get(pair[1])][position.get(pair[0])] = 1, 0
            else:
                matrix[position.get(pair[0])][position.get(pair[1])], matrix[position.get(pair[1])][position.get(pair[0])] = 0, 1
        return matrix 
    
    def aggregate_matrix(matrix: list) -> list:
        row_tally = []
        for row in range(len(matrix)):
            row_tally.append(sum(matrix[row]))
        
        col_tally = []
        for row in range(len(matrix)):
            total = 0
            for col in range(len(matrix)):
                total += matrix[col][row]
            col_tally.append(total)

        return row_tally, col_tally
    

    
if __name__ == "__main__":
    voting_profile = {
        "v1" : ["a", "c", "b", "f", "e", "d"],
        "v2" : ["b", "a", "d", "f", "c", "e"],
        "v3" : ["c", "f", "e", "b", "d", "a"],
        "v4" : ["d", "b", "f", "c", "a", "e"],
        "v5" : ["e", "f", "a", "c", "b", "d"],
        "v6" : ["e", "c", "d", "a", "f", "b"],
        "v7" : ["f", "d", "e", "c", "b", "a"]
    }

    alternatives = ("a", "b", "c", "d", "e", "f")

    load_rule = voting_rules(voting_profile, alternatives)

    plurality_winner = load_rule.plurality()
    print("Plurality winner: {}" .format(plurality_winner))

    single_transferable_vote_winner = load_rule.single_transferable_vote()
    print("STV winner: {}" .format(single_transferable_vote_winner))

    borda_winner = load_rule.borda_count()
    print("Borda winner: {}" .format(borda_winner))

    condorcet_winner = load_rule.condorcet_winner()
    print("Condorcet winner: {}" .format(condorcet_winner))

    copeland_winner = load_rule.copeland_winner()
    print("Copeland winner: {}" .format(copeland_winner))