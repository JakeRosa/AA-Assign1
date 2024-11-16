import matplotlib.pyplot as plt
import networkx as nx


# Sort the vertices of the graph in increasing order of degree
def sort_vertices(graph: nx.Graph):
    count = 0

    def merge(left, right):
        nonlocal count
        merged = []
        left_idx, right_idx = 0, 0

        while left_idx < len(left) and right_idx < len(right):
            count += 1
            if graph.degree(left[left_idx]) <= graph.degree(right[right_idx]):
                count += 1
                merged.append(left[left_idx])
                left_idx += 1
            else:
                count += 1
                merged.append(right[right_idx])
                right_idx += 1

        # Extend the remaining elements of the lists
        merged.extend(left[left_idx:])
        merged.extend(right[right_idx:])
        count += len(left[left_idx:]) + len(right[right_idx:])
        return merged
    
    def merge_sort(nodes):
        if len(nodes) <= 1:
            return nodes
        
        mid = len(nodes) // 2
        left = merge_sort(nodes[:mid])
        right = merge_sort(nodes[mid:])
        return merge(left, right)
    
    return merge_sort(list(graph.nodes)), count


# Find an independent set using a greedy heuristic approach that selects vertices with the lowest degree
def greedy_heuristic_independent_set(graph: nx.Graph):
    sorted_vertices, count = sort_vertices(graph)

    max_independent_set = set()
    neighbors_to_skip = set()  # Set of neighbors to skip

    for v in sorted_vertices:
        count += 1
        if v not in neighbors_to_skip:
            count += 1

            max_independent_set.add(v) # Add the vertex to the independent set 

            neighbors_to_skip.update(graph.neighbors(v)) # Add neighbors to the set of vertices to skip
            count += len(graph[v])
    
    return max_independent_set, count

# def plot_graph(graph, title, filename):
#     plt.figure(figsize=(5, 5))
#     pos = nx.spring_layout(graph, seed=42)  # Posição dos nós para visualização consistente
#     nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_size=10)
#     plt.title(title)
#     plt.savefig(filename)  # Salva o gráfico em um arquivo
#     plt.close()  # Fecha a figura para liberar memória

# # Função principal para testar o algoritmo e visualizar os grafos
# def test_maximum_independent_set():
#     # Criar exemplos de grafos
#     test_graphs = {
#         "Graph 1 - Simple Chain": nx.path_graph(5),
#         "Graph 2 - Complete Graph": nx.complete_graph(4),
#         "Graph 3 - Star Graph": nx.star_graph(4),
#         "Graph 4 - Bipartite Graph": nx.complete_bipartite_graph(3, 3),
#         "Graph 5 - Empty Graph": nx.empty_graph(5),
#     }

#     for name, graph in test_graphs.items():
#         print(f"Testing {name}:")
#         max_set, operations = greedy_heuristic_independent_set(graph)
#         print(f"Maximum Independent Set: {max_set}")
#         print(f"Number of Operations: {operations}")
#         print(f"Size of Independent Set: {len(max_set)}\n")
#         plot_graph(graph, name, f"{name.replace(' ', '_')}.png")

# # Rodar os testes
# if __name__ == "__main__":
#     test_maximum_independent_set()
