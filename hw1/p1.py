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
        # Get most frequently occurring first choice
        counts = utils.count_first_choice(self.profile)

        # Return top choice by most candidates
        return utils.select_winner(counts)
    
    def single_transferable_vote(self) -> str: 
        '''
            This implements the STV voting rule with a tie breaking rule to determine loser
        '''           
        num_voters = self.NUM_VOTERS
        upper_echelon = self.profile
        
        # Repeat until termination
        while True:
            # Get most frequently occurring first choice
            counts = utils.count_first_choice(upper_echelon)

            # Check if there is a clear majority or if there are only two candidates left
            if utils.got_majority(counts, num_voters) == True or len(counts.keys()) == 2:
                # Get maximal choice 
                return utils.select_winner(counts)
            
            # Get the candidate with the lowest tallied votes 
            lowest = utils.get_lowest_candidate(counts)

            # Check if there is more than one 'low' candidate
            if len(lowest) > 1:
                # Get the lowest echelon in case there is more than one low candidate (i.e, every candidate except the top one)
                lower_echelon = utils.update_profile(lowest, upper_echelon, eliminate=False)

                # Apply tie-breaker rule and now narrow down lowest candidate (this should return a filtered lowest candidate based on the tie breaker)
                lowest = utils.tie_breaker(lowest, lower_echelon, num_voters)

            # Elminiate the lowest candidate and redistribute voting portfolio to the remaining voters
            upper_echelon = utils.update_profile(lowest, upper_echelon, eliminate = True)
    
    def borda_count(self) -> str:
        '''
            This implements the Borda count rule
        '''
        # Initialize score dictionary
        score = {alternatives : 0 for alternatives in self.alternatives}
        # Iterate over each voter, ballot pair
        for _, preferences in self.profile.items():
            # Use (n-1, n-2, ...., 0) as the weight vector (computed based on length of preference), update score dictionary based on preference ordering
            score = utils.map_alternative_to_score(preferences, score)
        
        # Return maximal candidate (highest count here corresponds to highest Borda count)
        return utils.select_winner(score)
    
    def approval_voting(self) -> str:
        '''
            This implements approval voting
        '''
        matrix = []
        for idx, (_, preference) in enumerate(self.profile.items()):
            # Identify even voters
            if (idx + 1) % 2 == 0:
                # Net zero between position 2 and 3
                # Create a score vector e.g [(a, 1), (b, 1), (c, 0), .... ,(z, 0)]
                score = [(preference[elem], 1 if elem < 2 else 0) for elem in range(len(preference))]
                # Lexicographic sorting
                score = sorted(score)
            # Identify odd voters
            else:
                # Net zero between position 4 and 5
                # Create a score vector e.g [(a, 1), (b, 1), (c, 1), (d, 1), (e, 0), .... ,(z, 0)]
                score = [(preference[elem], 1 if elem < 4 else 0) for elem in range(len(preference))]
                # Lexicographic sorting 
                score = sorted(score)
            # Store all score vectors 
            matrix.append(score)
            # print(matrix)

        # Initialize approval aggregator
        approval = {alternative : 0 for alternative in self.alternatives}

        # Iterate by col
        for i in range(len(matrix[0])):
            # Iterate by row
            for j in range(len(matrix)):
                # update alternative score 
                approval[matrix[j][i][0]] = approval[matrix[j][i][0]] + matrix[j][i][1]
        # Get maximal winner 
        return utils.select_winner(approval)
    
    def condorcet_winner(self) -> str:
        '''
            This does all pair wise comparisons to determine if an alternative is preferred to ALL other alternatives
        '''
        # Create all combinations of pair tuples, set score to 0
        all_pairs = {pair: 0 for pair in itertools.combinations(self.alternatives,2)}

        # Create a mutable set 
        mutable_alternatives = set(self.alternatives)

        # Iterate over each profile
        for _, preference in self.profile.items():
            # Update all pairs (score dictionary for each pair), with how many times the pair wins
            # e.g, (a, b) = 4 means a wins against b 4 times. 
            # Also note that these are not all pairs but exactly half of them (combinations not permutations) as if one pair wins by majority the converse will not win
            # i.e if |(a,b)| > majority then |(b, a)| < majority 
            all_pairs = utils.get_pairwise_score(all_pairs, preference)
        

        blacklisted_candidates = set()
        
        # Iterate over each pair
        for pair, score in all_pairs.items():
            # If the pair did not get majority wins or if the pair's leading element is already blacklisted, add candidate 
            if score < int(self.NUM_VOTERS/2) + 1 or pair[0] in blacklisted_candidates:
                blacklisted_candidates.add(pair[0])
                continue

        # Do set difference to get how many candidates won pair wise 
        remaining_candidates = mutable_alternatives.difference(blacklisted_candidates)   
        
        # Ideal case, only one candidate is all pair wise winner          
        if len(remaining_candidates) == 1:
            return remaining_candidates.pop()  
        # This should return no clear candidate (more than 1)
        else:
            print("no clear condorcet winner")
            return remaining_candidates
        
    def copeland_winner(self) -> str:
        '''
            This implements Copeland's voting rule 
        '''
        # Same as in condorcet_winner, initialize all pair dictionary
        all_pairs = {pair: 0 for pair in itertools.combinations(self.alternatives, 2)}

        # Same as condorcet_winner
        for _, preference in self.profile.items():
            all_pairs = utils.get_pairwise_score(all_pairs, preference)

        
        initial = {self.alternatives[i]: i for i in range(len(self.alternatives))}

        # Get a score matrix based on all pairs
        matrix = utils.generate_matrix(all_pairs, set(self.alternatives), initial, self.NUM_VOTERS)

        # Tally candidates by row, tally candidates by column
        row_agg, col_agg = utils.aggregate_matrix(matrix)

        # Create a score dictionary that stores the difference between row aggregate - column aggregate (Copeland's defining feature) for each alternative
        diff = dict(map(lambda x, y, z: (z, x - y), row_agg, col_agg, self.alternatives))

        # Return maximal element
        return utils.select_winner(diff)

class utils:
    '''
        This is just a helper class for doing incredibly inefficient things
    '''

    def count_first_choice(profile: dict) -> dict:
        '''
            Iterate over each top choice and tally number of times the choice occurs
        '''
        counts = {}
        for _, preference in profile.items():
            first_choice = preference[0]
            if first_choice in counts.keys():
                counts[first_choice] += 1
            else:
                counts[first_choice] = 1
        return counts 

    def get_lowest_candidate(counts: dict) -> str:
        '''
            Determine the minimally scoring candidate(s) and return 
        '''
        lowest_candidates = {key for key in counts if counts.get(key) == min(counts.values())}
        if len(lowest_candidates) > 1:
            return lowest_candidates
        else:
            return lowest_candidates.pop()
    
    def got_majority(counts: dict, num_voters: int) -> bool:
        '''
            Check if there is a candidate with majority win
        '''
        if max(counts.values()) > int(num_voters/2) + 1:
            return True
        else:
            return False
        
    def update_profile(lowest: set, profile: dict, eliminate: bool) -> dict:
        '''
            Return voter profile for two cases:
                1) eliminate = True -> remove lowest candidate, redistribute votes and return profile
                2) eliminate = False -> get profile of only the tail candidates i.e, non-winners (this could probably have been done in a better way)
        '''
        new_profile = {}
        for voter, preference in profile.items():
            if eliminate:
                new_preference = list(filter(lambda x: x != lowest, preference))
            else:
                new_preference = list(filter(lambda x: x in lowest, preference))
            new_profile[voter] = new_preference
        return new_profile
    
    def select_winner(counts: dict) -> str:
        ''' 
            Return maximal voted candidate
        '''
        return {key for key in counts if counts.get(key) == max(counts.values())}.pop()

    def map_alternative_to_score(preference: list, score: dict) -> dict:
        '''
            Take each alternative, and update score dictionary with its weight by Borda rule
        '''
        for alternative, _ in score.items():
            score[alternative] = score[alternative] + ((len(preference) - 1) - preference.index(alternative))
        return score
        
    def tie_breaker(lowest: set, profile: dict, num_voters: int) -> str:
        '''
            This is a top cycle criterion but for removing the lowest scoring candidate
        '''
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
        '''
            Determine pair wise winner, then update score to get aggregate pair wise wins
        '''
        for pair, _ in pairs.items():
            if (preference.index(pair[0]) > preference.index(pair[1])):
                offset = 0
            else:
                offset = 1
            pairs[pair] = pairs[pair] + offset 
        return pairs
    
    def generate_matrix(pairs: dict, lowest: set, position: dict, num_voters: int) -> list:
        '''
            Generate an NxN matrix of 1's and 0's where each position checks if the score beat majority 
            If majority was achieved, 1 else 0 (this takes care of the reverse pair as well)
        '''
        matrix = [[0 for _ in range(len(lowest))] for _ in range(len(lowest))]
        for pair, score in pairs.items():
            if score >= int(num_voters/2) + 1:
                matrix[position.get(pair[0])][position.get(pair[1])], matrix[position.get(pair[1])][position.get(pair[0])] = 1, 0
            else:
                matrix[position.get(pair[0])][position.get(pair[1])], matrix[position.get(pair[1])][position.get(pair[0])] = 0, 1
        return matrix 
    
    def aggregate_matrix(matrix: list) -> list:
        '''
            Matrix aggregator (row wise and col wise) but unfortunately this is only for an N x N matrix
        '''
        row_tally = []
        for row in range(len(matrix[0])):
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

    approval_winner = load_rule.approval_voting()
    print("Approval winner: {}" .format(approval_winner))

    condorcet_winner = load_rule.condorcet_winner()
    print("Condorcet winner: {}" .format(condorcet_winner))

    copeland_winner = load_rule.copeland_winner()
    print("Copeland winner: {}" .format(copeland_winner))