import math
from individual import Individual

def greedy_algorithm(distance_matrix, demands, capacity):
    num_cities = len(demands)
    unvisited = set(range(1, num_cities))  # pomijamy depot (0)
    current_city = 0
    route = []
    remaining_capacity = capacity

    while unvisited:
        nearest = None
        nearest_dist = math.inf

        for city in unvisited:
            if demands[city] <= remaining_capacity:
                dist = distance_matrix[current_city][city]
                if dist < nearest_dist:
                    nearest = city
                    nearest_dist = dist

        if nearest is None:
            # Nie da się nigdzie jechać – wracamy do depotu
            current_city = 0
            remaining_capacity = capacity
        else:
            route.append(nearest)
            remaining_capacity -= demands[nearest]
            current_city = nearest
            unvisited.remove(nearest)

    indiv = Individual(route, capacity, demands)
    indiv.evaluate(distance_matrix)
    return indiv
