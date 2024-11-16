from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx


def is_independent_set(graph, vertices_set):
    count = 0   # Count the number of operations

    for v1, v2 in combinations(vertices_set, 2):  # all possible pairs of vertices
        count += 1
        if graph.has_edge(v1, v2):
            count += 1
            return False, count

    count += 1
    return True, count


def exhaustive_search_independent_set(graph):
    count = 0   # Count the number of operations
    n = len(graph.nodes)
    max_set = set()

    # Iterate over subsets in decreasing size order
    for size in range(n, 0, -1):
        for vertices_subset in combinations(graph.nodes, size):
            is_independent, independent_count = is_independent_set(graph, vertices_subset)
            count += independent_count

            if is_independent:
                count += 1
                return set(vertices_subset), count  # Return the first maximum independent set found

    return max_set, count


# def plot_graph(graph, title, filename):
#     plt.figure(figsize=(5, 5))
#     pos = nx.spring_layout(graph, seed=42)  # Posição dos nós para visualização consistente
#     nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_size=10)
#     plt.title(title)
#     plt.savefig(filename)  # Salva o gráfico em um arquivo
#     plt.close()  # Fecha a figura para liberar memória

# def test_maximum_independent_set():
#     test_graphs = {
#         "Graph 1 - Simple Chain": nx.path_graph(5),
#         "Graph 2 - Complete Graph": nx.complete_graph(4),
#         "Graph 3 - Star Graph": nx.star_graph(4),
#         "Graph 4 - Bipartite Graph": nx.complete_bipartite_graph(3, 3),
#         "Graph 5 - Empty Graph": nx.empty_graph(5),
#     }

#     for name, graph in test_graphs.items():
#         print(f"Testing {name}:")
#         max_set, operations = exhaustive_search_independent_set(graph)
#         print(f"Maximum Independent Set: {max_set}")
#         print(f"Number of Operations: {operations}")
#         print(f"Size of Independent Set: {len(max_set)}\n")
#         plot_graph(graph, name, f"{name.replace(' ', '_')}.png")

# if __name__ == "__main__":
#     test_maximum_independent_set()