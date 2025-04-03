import math
import random
from individual import Individual
from operators import swap_mutation, inversion_mutation

def simulated_annealing(distance_matrix, demands, capacity,
                        initial_temperature=1000, cooling_rate=0.999,
                        max_evaluations=100000, mutation_type='swap'):

    num_cities = len(demands)
    city_indices = list(range(1, num_cities))  # pomijamy depot

    # Inicjalizacja losowego rozwiązania
    random.shuffle(city_indices)
    current = Individual(city_indices[:], capacity, demands)
    current.evaluate(distance_matrix)
    best = current.copy()

    temperature = initial_temperature
    fitness_history = []
    evaluations = 0
    iteration = 0
    while evaluations < max_evaluations:
        # Tworzymy sąsiada (kopiujemy i mutujemy)
        neighbor = current.copy()

        if mutation_type == 'inversion':
            inversion_mutation(neighbor)
        else:
            swap_mutation(neighbor)

        neighbor.evaluate(distance_matrix)
        evaluations += 1
        delta = neighbor.fitness - current.fitness

        # Akceptujemy lepsze lub gorsze z prawdopodobieństwem zależnym od T
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbor

        # Aktualizacja najlepszego
        if current.fitness < best.fitness:
            best = current.copy()

        # Chłodzenie
        temperature *= cooling_rate

        # Zbieranie danych
        if iteration % 100 == 0:
            fitness_history.append((evaluations, best.fitness))

    return best, fitness_history
