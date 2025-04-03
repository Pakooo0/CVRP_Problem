import random
from individual import Individual

def random_search(distance_matrix, demands, capacity, evaluations=10000):
    num_cities = len(demands)
    city_indices = list(range(1, num_cities))  # pomijamy depot

    best = None

    for _ in range(evaluations):
        random.shuffle(city_indices)
        indiv = Individual(city_indices[:], capacity, demands)
        indiv.evaluate(distance_matrix)

        if best is None or indiv.fitness < best.fitness:
            best = indiv.copy()

    return best
