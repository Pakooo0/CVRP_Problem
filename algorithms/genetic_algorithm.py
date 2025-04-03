import random
from individual import Individual
from operators import swap_mutation, inversion_mutation, ordered_crossover, tournament_selection

def genetic_algorithm(distance_matrix, demands, capacity, pop_size=100,
                      crossover_prob=0.7, mutation_prob=0.1, tournament_size=5,
                      mutation_type='inversion', max_evaluations=10000):

    num_cities = len(demands)
    city_indices = list(range(1, num_cities))  # bez depotu

    # Tworzenie początkowej populacji
    population = []
    evaluations = 0
    for _ in range(pop_size):
        random.shuffle(city_indices)
        indiv = Individual(city_indices[:], capacity, demands)
        indiv.evaluate(distance_matrix)
        evaluations += 1
        population.append(indiv)

    best_overall = min(population, key=lambda ind: ind.fitness).copy()
    fitness_history = []
    gen = 0

    while evaluations < max_evaluations:
        new_population = []

        while len(new_population) < pop_size and evaluations < max_evaluations:
            # Selekcja
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)

            # Crossover
            if random.random() < crossover_prob:
                child_solution = ordered_crossover(parent1, parent2)
            else:
                child_solution = parent1.solution[:]

            # Tworzenie osobnika
            child = Individual(child_solution, capacity, demands)

            # Mutacja
            if random.random() < mutation_prob:
                if mutation_type == 'inversion':
                    inversion_mutation(child)
                else:
                    swap_mutation(child)

            # Ewaluacja
            child.evaluate(distance_matrix)
            evaluations += 1
            new_population.append(child)

        # Aktualizacja populacji
        population = new_population
        current_best = min(population, key=lambda ind: ind.fitness)

        if current_best.fitness < best_overall.fitness:
            best_overall = current_best.copy()

        # Zbieranie statystyk co 100 ocen
        if evaluations % 100 == 0:
            avg_fit = sum(ind.fitness for ind in population) / pop_size
            worst_fit = max(ind.fitness for ind in population)
            fitness_history.append((evaluations, best_overall.fitness, avg_fit, worst_fit))
            #print(f"Eval {evaluations}/{max_evaluations} - Best: {best_overall.fitness:.2f}, Avg: {avg_fit:.2f}")

        gen += 1

    return best_overall, fitness_history
