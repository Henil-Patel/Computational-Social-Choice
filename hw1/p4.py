def load_and_extract_file(file_name: str) -> tuple:
    '''
        $ The purpose of this method is to provide a convenient data structure based on input data
        $ For fun, I attempted my hand at functional programming! :) 
        $ Input: dataset.txt (or a text file with a certain format)
        $ Output: weight vector (read in as is - no transpose required)
                  profile matrix (list of list - inner list representing a ballot - transpose required) 
    '''
    # Read file, store to dataset var
    with open(file=file_name, mode="r") as f:
        dataset = f.readlines()
    
    # Refine each string to remove spaces and new line characters
    dataset = list(map(lambda x: x.replace(" ", "").rstrip("\n"), dataset))    
    
    # Take only the sublists which have length > 1 (these are rows of profiles)
    profile = list(map(lambda x: list(map(lambda z: str(z), x)) , filter(lambda y: len(y) > 1, dataset)))
    
    # This is the transpose (this converst the list from rows of profiles (positions) to a preference ordering)
    profile = [[profile[j][i] for j in range(len(profile))] for i in range(len(profile[0]))]
    
    # These are just single element sublists (presumably they are the weight vectors)
    weight = list(map(lambda x: int(x), filter(lambda y: len(y) == 1, dataset)))
    
    return profile, weight 

def compute_positional_score(profile: list, weight: list) -> str:
    '''
        $ This method applies the positional voting rule 
            $ Initially it defines a score dictionary where the keys are the alternatives and values are zeros
            $ Iterate over each element of profile -> update score dictionary by accessing keys
            $ Return alternative with highest score 
        $ I was not able to do purely functional programming here :(
        $ Input: profile, weight vector
        $ Output: the winning candidate
    '''

    score = {element: 0 for element in profile[0]}

    for i in range(len(profile)):
        for j in range(len(profile[i])):
            score[profile[i][j]] = score[profile[i][j]] + weight[j]

    return max(score.items(), key=lambda x: x[1])[0]
    
    
if __name__ == "__main__":
    # Entry point - PLEASE MAKE SURE TO SPECIFY DATASET FILE HERE
    profile, weight = load_and_extract_file("dataset.txt")
    
    # Uncomment below line for printing purposes
    # print(profile, weight)

    # Make the call and determine the winner
    winner = compute_positional_score(profile, weight)
    print("The [positional scoring rule] winner is: {}" .format(winner))