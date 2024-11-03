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
    
    def map_alternative_to_score(preference: list, score: dict) -> dict:
        '''
            Take each alternative, and update score dictionary with its weight by Borda rule
        '''
        for alternative, _ in score.items():
            score[alternative] = score[alternative] + ((len(preference) - 1) - preference.index(alternative))
        return score
    
if __name__ == "__main__":
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