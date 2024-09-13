def load_and_extract_file(file_name: str) -> tuple:

    with open(file=file_name, mode="r") as f:
        dataset = f.readlines()
    
    dataset = list(map(lambda x: x.replace(" ", "").rstrip("\n"), dataset))    
    
    profile = list(map(lambda x: list(map(lambda z: str(z), x)) , filter(lambda y: len(y) > 1, dataset)))
    profile = [[profile[j][i] for j in range(len(profile))] for i in range(len(profile[0]))]
    
    weight = list(map(lambda x: int(x), filter(lambda y: len(y) == 1, dataset)))
    
    return profile, weight 

def compute_positional_score(profile: list, weight: list) -> str:
    score = {element: 0 for element in profile[0]}

    for i in range(len(profile)):
        for j in range(len(profile[i])):
            score[profile[i][j]] = score[profile[i][j]] + weight[j]

    return max(score.items(), key=lambda x: x[1])[0]
    
    
if __name__ == "__main__":
    profile, weight = load_and_extract_file("dataset.txt")
    print(profile, weight)
    winner = compute_positional_score(profile, weight)
    print(winner)