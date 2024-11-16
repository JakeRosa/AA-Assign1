import json
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def exponential_fit(x, a, b):
    return a * np.exp(b * x)


def plot_results_from_file(results_file, plots_folder, algorithm_name):
    os.makedirs(plots_folder, exist_ok=True)

    with open(results_file, "r") as file:
        results = json.load(file)

    if not results:
        print("No results to plot.")
        return

    # Organize data by edge density
    densities = [0.12, 0.25, 0.5, 0.75]
    data_by_density = {density: {"vertices": [], "execution_times": [], "operation_counts": [], "combinations": []}
                        for density in densities}

    for r in results.values():
        edge_density = r["edge_density"]
        if edge_density in densities:
            data_by_density[edge_density]["vertices"].append(r["vertices"])
            data_by_density[edge_density]["execution_times"].append(r["execution_time"])
            data_by_density[edge_density]["operation_counts"].append(r["operation_count"])
            if algorithm_name == "exhaustive" and "combinations" in r:
                data_by_density[edge_density]["combinations"].append(r["combinations"])

    # Execution Time vs Edge Density
    plt.figure(figsize=(10, 5))
    plt.scatter([r["edge_density"] for r in results.values()],
                [r["execution_time"] for r in results.values()],
                c=[r["vertices"] for r in results.values()],
                cmap="viridis", label="Vertices (color)")
    plt.colorbar(label="Number of Vertices")
    plt.xlabel("Edge Density")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Execution Time vs Edge Density ({algorithm_name})")
    plt.grid(True)
    plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_execution_vs_edge_density.png"))
    plt.close()

    # Number of Operations: Original Plot
    plt.figure(figsize=(10, 5))
    for density, data in data_by_density.items():
        sorted_indices = np.argsort(data["vertices"])
        sorted_vertices = np.array(data["vertices"])[sorted_indices]
        sorted_operations = np.array(data["operation_counts"])[sorted_indices]
        plt.plot(sorted_vertices, sorted_operations, marker="o", label=f"{int(density * 100)}% Edge Density")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Operation Count")
    plt.title(f"Operation Count vs Number of Vertices ({algorithm_name}) - Normal")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_operations_vs_vertices_normal.png"))
    plt.close()

    # Number of Operations: Logarithmic Scale
    if algorithm_name == "exhaustive":
        plt.figure(figsize=(10, 5))
        for density, data in data_by_density.items():
            sorted_indices = np.argsort(data["vertices"])
            sorted_vertices = np.array(data["vertices"])[sorted_indices]
            sorted_operations = np.array(data["operation_counts"])[sorted_indices]
            plt.plot(sorted_vertices, sorted_operations, marker="o", label=f"{int(density * 100)}% Edge Density")
        plt.yscale("log")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Operation Count (log scale)")
        plt.title(f"Operation Count vs Number of Vertices ({algorithm_name}) - Log Scale")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_operations_vs_vertices_log.png"))
        plt.close()

    # Number of Operations: Exponential Fit with Prediction
    if algorithm_name == "exhaustive":
        plt.figure(figsize=(10, 5))
        for density, data in data_by_density.items():
            sorted_indices = np.argsort(data["vertices"])
            sorted_vertices = np.array(data["vertices"])[sorted_indices]
            sorted_operations = np.array(data["operation_counts"])[sorted_indices]
            plt.plot(sorted_vertices, sorted_operations, marker="o", label=f"{int(density * 100)}% Edge Density")
            
            # Exponential Fit with Prediction
            if len(sorted_vertices) > 2:
                try:
                    popt, _ = curve_fit(exponential_fit, sorted_vertices, sorted_operations)
                    fitted_values = exponential_fit(sorted_vertices, *popt)
                    plt.plot(sorted_vertices, fitted_values, linestyle="--", label=f"Exp Fit {int(density * 100)}%")

                    # Prediction for the next 10 values
                    next_vertices = np.arange(sorted_vertices[-1] + 1, sorted_vertices[-1] + 11)
                    predicted_values = exponential_fit(next_vertices, *popt)
                    plt.plot(next_vertices, predicted_values, linestyle=":", label=f"Prediction {int(density * 100)}%")
                except RuntimeError as e:
                    print(f"Exponential fit failed for density {density * 100}%: {e}")

        plt.xlabel("Number of Vertices")
        plt.ylabel("Operation Count (Exponential Fit + Prediction)")
        plt.title(f"Operation Count vs Number of Vertices ({algorithm_name}) - Exponential Fit with Prediction")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_operations_vs_vertices_exp_with_prediction.png"))
        plt.close()

    # Execution Time vs Number of Vertices
    plt.figure(figsize=(10, 5))
    for density, data in data_by_density.items():
        sorted_indices = np.argsort(data["vertices"])
        sorted_vertices = np.array(data["vertices"])[sorted_indices]
        sorted_times = np.array(data["execution_times"])[sorted_indices]
        plt.plot(sorted_vertices, sorted_times, marker="o", label=f"{int(density * 100)}% Edge Density")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Execution Time vs Number of Vertices ({algorithm_name}) - Normal")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_execution_vs_vertices_normal.png"))
    plt.close()

    # Execution Time vs Number of Vertices: Logarithmic Scale
    if algorithm_name == "exhaustive":
        plt.figure(figsize=(10, 5))
        for density, data in data_by_density.items():
            sorted_indices = np.argsort(data["vertices"])
            sorted_vertices = np.array(data["vertices"])[sorted_indices]
            sorted_times = np.array(data["execution_times"])[sorted_indices]
            plt.plot(sorted_vertices, sorted_times, marker="o", label=f"{int(density * 100)}% Edge Density")
        plt.yscale("log")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Execution Time (seconds, log scale)")
        plt.title(f"Execution Time vs Number of Vertices ({algorithm_name}) - Log Scale")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_execution_vs_vertices_log.png"))
        plt.close()

    # Execution Time vs Number of Vertices: Exponential Fit with Prediction
    if algorithm_name == "exhaustive":
        plt.figure(figsize=(10, 5))
        for density, data in data_by_density.items():
            sorted_indices = np.argsort(data["vertices"])
            sorted_vertices = np.array(data["vertices"])[sorted_indices]
            sorted_times = np.array(data["execution_times"])[sorted_indices]
            plt.plot(sorted_vertices, sorted_times, marker="o", label=f"{int(density * 100)}% Edge Density")
            
            # Exponential Fit with Prediction
            if len(sorted_vertices) > 2:
                try:
                    popt, _ = curve_fit(exponential_fit, sorted_vertices, sorted_times)
                    fitted_values = exponential_fit(sorted_vertices, *popt)
                    plt.plot(sorted_vertices, fitted_values, linestyle="--", label=f"Exp Fit {int(density * 100)}%")

                    # Prediction for the next 10 values
                    next_vertices = np.arange(sorted_vertices[-1] + 1, sorted_vertices[-1] + 11)
                    predicted_values = exponential_fit(next_vertices, *popt)
                    plt.plot(next_vertices, predicted_values, linestyle=":", label=f"Prediction {int(density * 100)}%")

                    # Prediction for 40 vertices
                    prediction_for_40_vertices = exponential_fit(np.array([40]), *popt)
                    print(f"Predicted execution time for 40 vertices (density {density * 100}%): {prediction_for_40_vertices[0]} seconds")
                except RuntimeError as e:
                    print(f"Exponential fit failed for density {density * 100}%: {e}")

        plt.xlabel("Number of Vertices")
        plt.ylabel("Execution Time (Exponential Fit + Prediction)")
        plt.title(f"Execution Time vs Number of Vertices ({algorithm_name}) - Exponential Fit with Prediction")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_execution_vs_vertices_exp_with_prediction.png"))
        plt.close()


    # Number of Combinations vs Number of Vertices (Exhaustive Search)
    if algorithm_name == "exhaustive":
        plt.figure(figsize=(10, 5))
        for density, data in data_by_density.items():
            sorted_indices = np.argsort(data["vertices"])
            sorted_vertices = np.array(data["vertices"])[sorted_indices]
            sorted_combinations = np.array(data["combinations"])[sorted_indices]
            plt.plot(sorted_vertices, sorted_combinations, marker="o", label=f"{int(density * 100)}% Edge Density")
        plt.yscale("log")
        plt.xlabel("Number of Vertices")
        if algorithm_name == "exhaustive":
            plt.ylabel("Combinations (log scale)")
        elif algorithm_name == "greedy":
            plt.ylabel("Combinations")
        plt.title(f"Number of Combinations vs Number of Vertices ({algorithm_name})")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(plots_folder, f"{algorithm_name}_combinations_vs_vertices.png"))
        plt.close()

    print(f"Plots saved in '{plots_folder}'.")

if __name__ == "__main__":
    results_file = input("Enter the path to the results file (e.g., results/exhaustive_results.json): ").strip()
    plots_folder = input("Enter the folder to save plots (e.g., plots): ").strip()
    algorithm_name = input("Enter the algorithm name for plot titles and filenames (e.g., exhaustive): ").strip()

    # Validate the input
    if not os.path.isfile(results_file):
        print(f"Error: The file '{results_file}' does not exist.")
    else:
        # Generate the plots
        plot_results_from_file(results_file, plots_folder, algorithm_name)
