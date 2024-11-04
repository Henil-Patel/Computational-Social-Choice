import itertools
import string
import copy 

class modified_copeland:
    '''
        This class is modified for the purpose of determining whether a select candidate can be a copeland winner or not through constructive control
    '''

    def __init__(self, profile: dict, alternatives: tuple):
        '''
            Initialize class
        '''
        self.profile = profile
        self.NUM_VOTERS = len(self.profile.keys())
        self.alternatives = alternatives
        self.candidate_positions = {self.alternatives[i]: i for i in range(len(self.alternatives))}
        self.matrix = []
    
    def _generate_copeland_matrix(self) -> str:
        '''
            This will make the win loss matrix given the alternatives and pairwise scores
        '''
        # Same as in condorcet_winner, initialize all pair dictionary
        all_pairs = {pair: 0 for pair in itertools.combinations(self.alternatives, 2)}

        # Apply pairwise scores to the score dictionary for each pair
        for _, preference in self.profile.items():
            all_pairs = utils.get_pairwise_score(all_pairs, preference)

        # Get a score matrix based on all pairs
        return utils.generate_win_loss_matrix(all_pairs, set(self.alternatives), self.candidate_positions, self.NUM_VOTERS)
    
    def _determine_winner(self, matrix, alternatives):
        '''
            Helper for computing winner in case of Copeland voting rule
        '''
        # Tally candidates by row, tally candidates by column
        
        row_agg, col_agg = utils.get_row_col_scores(matrix)

        # Create a score dictionary that stores the difference between row aggregate - column aggregate (Copeland's defining feature) for each alternative
        diff = dict(map(lambda x, y, z: (z, x - y), row_agg, col_agg, alternatives))
        # print(diff)
        # Return maximal element
        return utils.select_winner(diff)
    
    def constructive_control_copeland_winner(self):
        '''
            This method iterates through each alternative and returns all the possible removals (at most 2) required to make a candidate a Copeland winner 
        '''
        # Generate matrix without deletions
        self.matrix = self._generate_copeland_matrix()

        # Get scores without deletions 
        raw_winners = self._determine_winner(self.matrix, self.alternatives)

        num_required_removals_to_win = {a: 0 for a in self.alternatives}

        # Each iteration represents target candidate to be made unique winner
        for target, idx in self.candidate_positions.items():
            # print(f"----------------{target}----------------")
            mutable_matrix = {i:{j: elem for j, elem in enumerate(row)} for i, row in enumerate(self.matrix)}
            target_outcome = mutable_matrix[idx]
            dominant = [k for k,v in target_outcome.items() if v == 0]
            # # Remove target to avoid comparing with itself
            dominant.remove(idx)
            dominion = [k for k,v in target_outcome.items() if v == 1]
            corresponding_candidates = [k for k,v in self.candidate_positions.items() if v in dominant]
            mutable_alternatives = list(copy.deepcopy(self.alternatives))
            num_removals = 0
            for winner in dominant:
                _ = {k for k,v in self.candidate_positions.items() if v == winner}.pop()
                # Remove row
                mutable_matrix.pop(winner)
                num_removals += 1
                # Remove column
                for k,v in mutable_matrix.items():
                    v.pop(winner)
                usable_matrix = [list(v.values()) for k, v in mutable_matrix.items()]
                mutable_alternatives.remove(_)
                new_raw_winners = self._determine_winner(usable_matrix, mutable_alternatives)
                # print(new_raw_winners)
                if target in new_raw_winners and len(new_raw_winners) == 1:
                    num_required_removals_to_win.update({target:num_removals})
        return num_required_removals_to_win
            



    
class utils:
    '''
        This is just a helper class for doing incredibly inefficient things
    '''
    def select_winner(counts: dict) -> str:
        ''' 
            Return maximal voted candidate
        '''
        return {key for key in counts if counts.get(key) == max(counts.values())}
    
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
    
    def generate_win_loss_matrix(pairs: dict, lowest: set, position: dict, num_voters: int) -> list:
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
    
    def get_row_col_scores(matrix: list) -> list:
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
    # Voting Profile from problem 3(a)
    P_2 = {
        "v1" : ["b", "e", "g", "i", "h", "a", "c", "d", "f"],
        "v2" : ["a", "h", "b", "i", "e", "d", "g", "c", "f"],
        "v3" : ["h", "b", "f", "e", "c", "i", "a", "d", "g"],
        "v4" : ["e", "h", "b", "a", "i", "c", "d", "g", "f"],
        "v5" : ["h", "i", "b", "e", "g", "f", "c", "a", "d"],
        "v6" : ["b", "i", "h", "e", "g", "f", "a", "d", "c"],
        "v7" : ["b", "a", "i", "e", "h", "g", "d", "f", "c"],
        "v8" : ["e", "i", "h", "b", "f", "a", "d", "g", "c"]
    }

    A_2 = tuple(string.ascii_lowercase[string.ascii_lowercase.index('a'):string.ascii_lowercase.index('i')+1])

    MC = modified_copeland(P_2, A_2)
    removals_count = MC.constructive_control_copeland_winner()
    print(removals_count)
