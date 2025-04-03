import random

def swap_mutation(individual):
    """Losowo zamienia dwa miasta w trasie"""
    i, j = random.sample(range(len(individual.solution)), 2)
    individual.solution[i], individual.solution[j] = individual.solution[j], individual.solution[i]

def inversion_mutation(individual):
    """Odwraca losowy fragment trasy"""
    i, j = sorted(random.sample(range(len(individual.solution)), 2))
    individual.solution[i:j+1] = individual.solution[i:j+1][::-1]

def ordered_crossover(parent1, parent2):
    """Ordered Crossover (OX)"""
    size = len(parent1.solution)
    child_solution = [None] * size

    # Wybierz losowy fragment z rodzica 1
    start, end = sorted(random.sample(range(size), 2))
    child_solution[start:end+1] = parent1.solution[start:end+1]

    # Uzupełnij resztę genami z rodzica 2 w kolejności
    fill_values = [gene for gene in parent2.solution if gene not in child_solution]
    pos = 0
    for i in range(size):
        if child_solution[i] is None:
            child_solution[i] = fill_values[pos]
            pos += 1

    # Zwracamy nowego osobnika – trzeba ręcznie ustawić resztę pól
    return child_solution

def tournament_selection(population, tournament_size):
    """Zwraca najlepszego osobnika z losowej grupy"""
    competitors = random.sample(population, tournament_size)
    return min(competitors, key=lambda ind: ind.fitness)
