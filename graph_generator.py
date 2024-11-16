import json
import os

import networkx as nx

SEED = 109089
OUTPUT_FOLDER = "graphs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Generate a graph using the fast_gnp_random_graph method from NetworkX
def generate_graph(num_vertices, edge_density):
    return nx.fast_gnp_random_graph(num_vertices, edge_density, seed=SEED)

# Save the graph in JSON format with the adjacency list
def save_graph(graph, num_vertices, edge_percent):
    adjacency_list = {str(node): [str(neighbor) for neighbor in graph.neighbors(node)] for node in graph.nodes}
    filename = os.path.join(OUTPUT_FOLDER, f"graph_{num_vertices}_{edge_percent}.json")
    with open(filename, "w") as file:
        json.dump(adjacency_list, file, indent=4)

# Generate and save graphs with different edge densities
def generate_and_save_graphs():
    edge_densities = [0.125, 0.25, 0.5, 0.75]  # Densities of 12.5%, 25%, 50%, and 75%
    for num_vertices in range(4, 501):  # Number of vertices from 4 to 501
        for density in edge_densities:
            G = generate_graph(num_vertices, density)
            save_graph(G, num_vertices, int(density * 100))
            print(f"Grafo gerado: {num_vertices} vértices, {int(density * 100)}% densidade.")

if __name__ == "__main__":
    generate_and_save_graphs()
