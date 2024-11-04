
import matplotlib.pyplot as plt 

def load_and_extract_file(file_name: str) -> tuple:
    '''
        $ Input: dataset.txt (or a text file with a certain format)
        $ Output: profile matrix (list of list - inner list representing a ballot - transpose required) 
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
    
    return profile 

def single_peaked_preference(profile, orderings):
    '''
        This method plots preferences based on the loaded preference
    '''
    # Iterate over orderings
    for idx, ordering in enumerate(orderings):
        # Iterate over each ballot
        for jdx, ballot in enumerate(profile):
            # Compute positions of each alternative given ballot
            positions = list(map(lambda x: ballot.index(x)+1, ordering))
            # Plot each computed position
            plt.plot(ordering, positions, marker='o', label=f"voter {jdx+1}")
        plt.gca().invert_yaxis()
        plt.xlabel(f"ordering $>^{({idx+1})}$")
        plt.ylabel("ranking")
        plt.legend(title="ballots")
        plt.show()
        


if __name__ == "__main__":
    # Entry point - PLEASE MAKE SURE TO SPECIFY DATASET FILE HERE BY PATH
    #               CURRENTLY THIS ASSUMES .TXT FILE EXISTS IN THE SAME DIRECTORY
    profile = load_and_extract_file("profile.txt")
    orderings = load_and_extract_file("orderings.txt")
    
    # Uncomment below line for printing purposes
    # print(profile)
    # print(orderings)

    # Call the plotting function
    single_peaked_preference(profile, orderings)
