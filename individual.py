import random

class Individual:
    def __init__(self, solution, capacity, demands, depot=0):
        self.solution = solution  # permutacja miast (bez depotu)
        self.fitness = None
        self.capacity = capacity
        self.demands = demands
        self.depot = depot

    def evaluate(self, distance_matrix):
        total_distance = 0
        route_capacity = 0
        current_city = self.depot
        for city in self.solution:
            demand = self.demands[city]
            if route_capacity + demand > self.capacity:
                # wracamy do depotu
                total_distance += distance_matrix[current_city][self.depot]
                current_city = self.depot
                route_capacity = 0
            total_distance += distance_matrix[current_city][city]
            route_capacity += demand
            current_city = city
        # powrót do depotu na końcu
        total_distance += distance_matrix[current_city][self.depot]
        self.fitness = total_distance
        return self.fitness

    def copy(self):
        new = Individual(self.solution[:], self.capacity, self.demands, self.depot)
        new.fitness = self.fitness
        return new
