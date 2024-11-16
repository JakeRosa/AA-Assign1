import json
import os

import matplotlib.pyplot as plt
import numpy as np


def plot_comparison(exhaustive_results_file, greedy_results_file, plots_folder):
    # Create the output folder if it does not exist
    os.makedirs(plots_folder, exist_ok=True)

    # Load the results from the JSON files
    with open(exhaustive_results_file, "r") as file:
        exhaustive_results = json.load(file)
    with open(greedy_results_file, "r") as file:
        greedy_results = json.load(file)

    total_graphs = len(exhaustive_results)
    matching_solutions = 0
    different_solutions = 0
    errors_by_vertices = {}
    errors_by_density = {}


    # Verifies the results of the greedy search
    for graph_id, exhaustive_data in exhaustive_results.items():
        exhaustive_set_size = exhaustive_data["set_size"]
        greedy_set_size = greedy_results.get(graph_id, {}).get("set_size", None)
        num_vertices = exhaustive_data["vertices"]
        edge_density = exhaustive_data["edge_density"]

        if greedy_set_size is not None:
            if exhaustive_set_size == greedy_set_size:
                matching_solutions += 1
            else:
                different_solutions += 1
                if num_vertices not in errors_by_vertices:
                    errors_by_vertices[num_vertices] = 0
                errors_by_vertices[num_vertices] += 1

                if edge_density not in errors_by_density:
                    errors_by_density[edge_density] = 0
                errors_by_density[edge_density] += 1

    # Plot comparison pie chart
    plt.figure(figsize=(8, 6))
    labels = ["Matching Solutions", "Different Solutions"]
    sizes = [matching_solutions, different_solutions]
    colors = ["lightgreen", "salmon"]

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title("Comparison of Greedy Search vs Exhaustive Search Results")
    plt.axis("equal") 
    plt.savefig(os.path.join(plots_folder, "comparison_greedy_vs_exhaustive.png"))
    plt.close()

    # Plot errors by number of vertices
    if errors_by_vertices:
        plt.figure(figsize=(10, 6))
        vertices = sorted(errors_by_vertices.keys())
        errors = [errors_by_vertices[v] for v in vertices]

        plt.bar(vertices, errors, color="salmon", edgecolor="black")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Number of Errors")
        plt.title("Errors Made by Greedy Search by Number of Vertices")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.xticks(vertices)
        plt.savefig(os.path.join(plots_folder, "greedy_errors_by_vertices.png"))
        plt.close()

    # Plot errors by edge density
    if errors_by_density:
        plt.figure(figsize=(10, 6))
        densities = [0.12, 0.25, 0.5, 0.75]  
        errors = [errors_by_density.get(d, 0) for d in densities] 

        # Align the bars to the center
        bar_width = 0.1  # Width of the bars
        plt.bar(densities, errors, width=bar_width, color="salmon", edgecolor="black", align="center")

        plt.xlabel("Edge Density")
        plt.ylabel("Number of Errors")
        plt.title("Errors Made by Greedy Search by Edge Density")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        
        # Set the x-axis ticks to the edge densities
        plt.xticks(densities, [f"{d:.2f}" for d in densities])
        
        plt.savefig(os.path.join(plots_folder, "greedy_errors_by_density.png"))
        plt.close()




    print(f"Comparison plots saved in '{plots_folder}'.")


if __name__ == "__main__":
    exhaustive_results_file = "results/exhaustive_results.json"
    greedy_results_file = "results/greedy_results.json"
    plots_folder = "plots"

    # Validate the existence of the results files
    if not os.path.isfile(exhaustive_results_file) or not os.path.isfile(greedy_results_file):
        print("Error: One or both of the results files do not exist.")
    else:
        # Generate the comparison plots
        plot_comparison(exhaustive_results_file, greedy_results_file, plots_folder)
