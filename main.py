import os
from instance_loader import read_vrp_instance
from algorithms.genetic_algorithm import genetic_algorithm
from algorithms.simulated_annealing import simulated_annealing
from algorithms.greedy import greedy_algorithm
from algorithms.random_search import random_search
# === Wczytanie instancji ===
instance_name = "A-n32-k5.vrp"
file_path = os.path.join("instances", instance_name)
distance_matrix, demands, capacity = read_vrp_instance(file_path)

# === Parametry GA ===
# Parametry GA
ga_params = {
    'pop_size': 100,
    'crossover_prob': 0.6,
    'mutation_prob': 0.2,
    'tournament_size': 5,
    'mutation_type': 'inversion',
    'max_evaluations': 100000
}


# === Parametry SA ===
sa_params = {
    'initial_temperature': 10000,
    'cooling_rate': 0.9999,
    'max_evaluations': 100000,
    'mutation_type': 'swap'
}

# === Uruchom GA ===
best_ga, history_ga = genetic_algorithm(
    distance_matrix=distance_matrix,
    demands=demands,
    capacity=capacity,
    **ga_params
)
print("\nNajlepszy wynik GA:", best_ga.fitness)

# === Uruchom SA ===
print("\n--- Simulated Annealing ---")
best_sa, history_sa = simulated_annealing(
    distance_matrix=distance_matrix,
    demands=demands,
    capacity=capacity,
    **sa_params
)
print("\nNajlepszy wynik SA:", best_sa.fitness)

# === Zapisz wyniki do plików ===
import csv

os.makedirs("logs", exist_ok=True)

with open("logs/fitness_history_ga.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Evaluation", "Best", "Average", "Worst"])
    for row in history_ga:
        writer.writerow(row)

with open("logs/fitness_history_sa.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Iteration", "Fitness"])
    for row in history_sa:
        writer.writerow(row)

# === Greedy ===
print("\n--- Greedy Algorithm ---")
greedy = greedy_algorithm(distance_matrix, demands, capacity)
print("Wynik Greedy:", greedy.fitness)

# === Random Search ===
print("\n--- Random Search ---")
evaluations = ga_params['max_evaluations']
rand = random_search(distance_matrix, demands, capacity, evaluations)
print("Wynik Random:", rand.fitness)