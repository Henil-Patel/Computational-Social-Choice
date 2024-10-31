import itertools
import string
import copy 
class voting_rules:

    def __init__(self, profile: dict, alternatives: tuple):
        '''
            Initialize class
        '''
        self.profile = profile
        self.NUM_VOTERS = len(self.profile.keys())
        self.alternatives = alternatives
    
    def copeland_winner(self):
        '''
            This implements Copeland's voting rule 
        '''
        # Same as in condorcet_winner, initialize all pair dictionary
        all_pairs = {pair: 0 for pair in itertools.combinations(self.alternatives, 2)}

        fifth_ballot = itertools.permutations(self.alternatives, len(self.alternatives))

        # Same as condorcet_winner
        for b5 in fifth_ballot:
            
            # Add fifth profile
            self.profile.update({"v5": list(b5)})
            
            # Same as in condorcet_winner, initialize all pair dictionary
            all_pairs = {pair: 0 for pair in itertools.combinations(self.alternatives, 2)}
            

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
            yield utils.select_winner(diff)
    
    def borda_count(self):
        '''
            This implements the Borda count rule
        '''
        all_possible_winners = []
        # Initialize score dictionary for total profile (this is before any changes are made to the profile)
        unaltered_score = {alternative : 0 for alternative in self.alternatives}
        # Iterate over each voter, ballot pair
        for _, preference in self.profile.items():
            # Use (n-1, n-2, ...., 0) as the weight vector (computed based on length of preference), update score dictionary based on preference ordering
            unaltered_score = utils.map_alternative_to_score(preference, unaltered_score)
        unaltered_winner = utils.select_winner(unaltered_score)
        all_possible_winners.append(unaltered_winner)
        mutable_profile = copy.deepcopy(self.profile)
        for voter, true_preference in self.profile.items():
            mutable_profile.pop(voter)
            altered_score = {alternative : 0 for alternative in self.alternatives}
            for _, preference in mutable_profile.items():
                # Use (n-1, n-2, ...., 0) as the weight vector (computed based on length of preference), update score dictionary based on preference ordering
                altered_score = utils.map_alternative_to_score(preference, altered_score)
            altered_winner = utils.select_winner(altered_score)
            all_possible_winners.append(altered_winner)
            mutable_profile.update({voter: true_preference})
        # Return maximal candidate (highest count here corresponds to highest Borda count)
        return all_possible_winners
    
class utils:
    '''
        This is just a helper class for doing incredibly inefficient things
    '''
    def select_winner(counts: dict) -> str:
        ''' 
            Return maximal voted candidate
        '''
        return {key for key in counts if counts.get(key) == max(counts.values())}.pop()
    
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
    
    def map_alternative_to_score(preference: list, score: dict) -> dict:
        '''
            Take each alternative, and update score dictionary with its weight by Borda rule
        '''
        for alternative, _ in score.items():
            score[alternative] = score[alternative] + ((len(preference) - 1) - preference.index(alternative))
        return score
    
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
    # Voting Profile from problem 2
    P_2 = {
        "v1" : ["b", "a", "d", "e", "c"],
        "v2" : ["e", "c", "b", "a", "d"],
        "v3" : ["a", "b", "c", "d", "e"],
        "v4" : ["e", "c", "b", "a", "d"]
    }

    A_2 = tuple(string.ascii_lowercase[string.ascii_lowercase.index('a'):string.ascii_lowercase.index('e')+1])

    load_rule = voting_rules(P_2, A_2)

    # Storing as a set to ensure uniqueness
    copeland_winner = set(load_rule.copeland_winner())
    print(f"Not possible Copeland winners: {set(A_2).difference(copeland_winner)}")
    print(f"Possible Copeland winners: {copeland_winner}")

    # Voting Profile from problem 3(a)

    P_1 = ["b,a,c,h,g,f,e,d",
           "a,b,g,f,h,c,e,d",
           "h,e,b,f,a,g,c,d",
           "b,h,g,a,e,f,c,d",
           "b,f,d,a,g,c,h,e",
           "d,g,f,e,a,h,b,c",
           "e,c,f,h,b,a,g,d",
           "d,b,a,g,f,c,h,e",
           "b,h,f,g,e,a,c,d"]
    
    A_1 = tuple(string.ascii_lowercase[string.ascii_lowercase.index('a'):string.ascii_lowercase.index('h')+1])
    P_1 = {"v"+str(idx+1): P_1[idx].split(",") for idx in range(len(P_1))}

    load_rule = voting_rules(P_1, A_1)
    borda_winner = set(load_rule.borda_count())
    print(f"Not possible Borda winners: {set(A_1).difference(borda_winner)}")
    print(f"Possible Borda winners: {borda_winner}")
