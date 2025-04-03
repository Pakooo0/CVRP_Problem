import matplotlib.pyplot as plt
import csv
import os

def read_ga_history(filepath):
    generations, bests, avgs, worsts = [], [], [], []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            generations.append(int(row['Evaluation']))
            bests.append(float(row['Best']))
            avgs.append(float(row['Average']))
            worsts.append(float(row['Worst']))
    return generations, bests, avgs, worsts

def read_sa_history(filepath):
    iterations, fitnesses = [], []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            iterations.append(int(row['Iteration']))
            fitnesses.append(float(row['Fitness']))
    return iterations, fitnesses

def plot_separate(ga_path, sa_path):
    gen, bests, avgs, worsts = read_ga_history(ga_path)
    iters, sa_fitness = read_sa_history(sa_path)

    # Tworzymy osobne figury
    plt.figure(figsize=(10, 5))
    plt.plot(gen, bests, label="Best", linewidth=2)
    plt.plot(gen, avgs, label="Average", linestyle='--')
    plt.plot(gen, worsts, label="Worst", linestyle=':')
    plt.title("Genetic Algorithm - Fitness over Evaluations")
    plt.xlabel("Evaluation")
    plt.ylabel("Fitness (distance)")
    plt.legend()
    plt.grid(True)
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/ga_plot.png")
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(iters, sa_fitness, label="SA - Fitness", color='red', linewidth=2)
    plt.title("Simulated Annealing - Fitness over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Fitness (distance)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/sa_plot.png")
    plt.show()

if __name__ == "__main__":
    plot_separate("logs/fitness_history_ga.csv", "logs/fitness_history_sa.csv")
