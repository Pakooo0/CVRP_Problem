import os
import statistics
from instance_loader import read_vrp_instance
from algorithms.genetic_algorithm import genetic_algorithm
from algorithms.simulated_annealing import simulated_annealing
from algorithms.greedy import greedy_algorithm
from algorithms.random_search import random_search

inst_names = ["A-n32-k5.vrp", "A-n37-k6.vrp", "A-n45-k6.vrp","A-n39-k5.vrp","A-n48-k7.vrp","A-n54-k7.vrp","A-n60-k9.vrp"]

ga_params = {
    'pop_size': 100,
    'crossover_prob': 0.6,
    'mutation_prob': 0.2,
    'tournament_size': 5,
    'mutation_type': 'inversion',
    'max_evaluations': 100000,
}

sa_params = {
    'initial_temperature': 10000,
    'cooling_rate': 0.9999,
    'max_evaluations': 100000,
    'mutation_type': 'swap'
}

results = []

for inst in inst_names:
    print(f"\n=== Instance: {inst} ===")
    path = os.path.join("instances", inst)
    distance_matrix, demands, capacity = read_vrp_instance(path)
    # GA - 10x
    ga_scores = []
    for _ in range(10):
        best, _ = genetic_algorithm(distance_matrix, demands, capacity, **ga_params)
        ga_scores.append(best.fitness)

    # SA - 10x
    sa_scores = []
    for _ in range(10):
        best, _ = simulated_annealing(distance_matrix, demands, capacity, **sa_params)
        sa_scores.append(best.fitness)

    # Random - 1x (tyle samo ewaluacji co GA)
    total_evals = ga_params['max_evaluations']
    rand = random_search(distance_matrix, demands, capacity, evaluations=total_evals)

    # Greedy - 1x
    greedy = greedy_algorithm(distance_matrix, demands, capacity)

    results.append([
        inst,
        min(ga_scores), max(ga_scores), statistics.mean(ga_scores), statistics.stdev(ga_scores),
        min(sa_scores), max(sa_scores), statistics.mean(sa_scores), statistics.stdev(sa_scores),
        rand.fitness,
        greedy.fitness
    ])

# Zapis do CSV
import csv
with open("results/summary_table.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "Instance",
        "GA_best", "GA_worst", "GA_avg", "GA_std",
        "SA_best", "SA_worst", "SA_avg", "SA_std",
        "Random",
        "Greedy"
    ])
    writer.writerows(results)

print("\n✅ Wyniki zapisane do results/summary_table.csv")
