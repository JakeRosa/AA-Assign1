import json
import os
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from exhaustive_search import exhaustive_search_independent_set
from greedy_search import greedy_heuristic_independent_set

GRAPHS_FOLDER = "graphs"
TIME_THRESHOLD = 120  # 2 minutes

# Load graphs from JSON files
def load_graphs(graphs_folder):
    graphs = {}
    for filename in os.listdir(graphs_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(graphs_folder, filename)
            with open(filepath, 'r') as file:
                adjacency_list = json.load(file)
                G = nx.Graph()
                for node, neighbors in adjacency_list.items():
                    node = tuple(map(int, node.strip('()').split(', ')))
                    G.add_node(node)
                    for neighbor in neighbors:
                        neighbor = tuple(map(int, neighbor.strip('()').split(', ')))
                        G.add_edge(node, neighbor)
            graph_id = filename.replace('graph_', '').replace('.json', '')
            graphs[graph_id] = G
    return graphs

# Execute the algorithm on each graph and collect performance metrics
def run_experiments(graphs, algo, time_threshold, algorithm_name):
    results = {}
    largest_processable_graph = None

    for graph_id in sorted(graphs.keys(), key=lambda x: int(x.split('_')[0])):
        print(f"Testing graph {graph_id} with {algorithm_name}...")

        start_time = time.perf_counter()
        try:
            max_set, operation_count = algo(graphs[graph_id])
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time

            if elapsed_time > time_threshold:
                print(f"Graph {graph_id} took too long to process ({elapsed_time:.2f}s). Terminating experiments...")
                break 

            num_vertices = int(graph_id.split('_')[0])
            edge_density = float(graph_id.split('_')[1]) / 100

            # Result structure
            result = {
                "vertices": num_vertices,
                "edge_density": edge_density,
                "execution_time": elapsed_time,
                "operation_count": operation_count,
                "set_size": len(max_set),
            }

            # For the exhaustive search algorithm, calculate the number of combinations
            if algorithm_name == "Exhaustive Search":
                result["combinations"] = 2 ** num_vertices

            results[graph_id] = result
            largest_processable_graph = graph_id

        except Exception as e:
            print(f"Error processing graph {graph_id} with {algorithm_name}: {e}")
            break  

    return results, largest_processable_graph

if __name__ == "__main__":
    graphs = load_graphs(GRAPHS_FOLDER)

    # Results dictionary to store all results
    all_results = {}

    # Run experiments for the exhaustive search algorithm
    print("\nRunning experiments for Exhaustive Search...")
    exhaustive_results, largest_exhaustive_graph = run_experiments(
        graphs, exhaustive_search_independent_set, TIME_THRESHOLD, "Exhaustive Search"
    )
    if exhaustive_results:
        os.makedirs("results", exist_ok=True)
        with open("results/exhaustive_results.json", "w") as file:
            json.dump(exhaustive_results, file, indent=4)
        print(f"Largest graph processed with Exhaustive Search: {largest_exhaustive_graph}")
        all_results["exhaustive"] = exhaustive_results

    # Run experiments for the greedy search algorithm
    print("\nRunning experiments for Greedy Search...")
    greedy_results, largest_greedy_graph = run_experiments(
        graphs, greedy_heuristic_independent_set, TIME_THRESHOLD, "Greedy Search"
    )
    if greedy_results:
        os.makedirs("results", exist_ok=True)
        with open("results/greedy_results.json", "w") as file:
            json.dump(greedy_results, file, indent=4)
        print(f"Largest graph processed with Greedy Search: {largest_greedy_graph}")
        all_results["greedy"] = greedy_results

    # Save all results
    if all_results:
        with open("results/all_results.json", "w") as file:
            json.dump(all_results, file, indent=4)

    print("\nExperiments completed!")
