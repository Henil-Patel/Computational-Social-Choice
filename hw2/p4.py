import networkx as nx
import matplotlib.pyplot as plt

def generate_graph(adjacency_matrix: list, G):
    mapping = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g'}
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] == 1:
                G.add_edge(mapping[i], mapping[j])

    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels = True, node_color = "skyblue", node_size = 2000, edge_color = "black", arrows = True, font_size = 15)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    print(dir(G))
    # plt.show()

if __name__ == "__main__":
    adjacency_matrix = [
        [0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0]
    ]

    G = nx.DiGraph()
    generate_graph(adjacency_matrix, G)
