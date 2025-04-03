import math

def read_vrp_instance(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    node_coord_section = False
    demand_section = False
    depot_section = False

    coords = {}
    demands = {}
    depot = None
    capacity = None

    for line in lines:
        line = line.strip()

        if "CAPACITY" in line:
            capacity = int(line.split()[-1])

        if line.startswith("NODE_COORD_SECTION"):
            node_coord_section = True
            continue
        elif line.startswith("DEMAND_SECTION"):
            node_coord_section = False
            demand_section = True
            continue
        elif line.startswith("DEPOT_SECTION"):
            demand_section = False
            depot_section = True
            continue
        elif line.startswith("EOF"):
            break

        if node_coord_section:
            parts = line.split()
            idx = int(parts[0])
            coords[idx] = (float(parts[1]), float(parts[2]))
        elif demand_section:
            parts = line.split()
            idx = int(parts[0])
            demands[idx] = int(parts[1])
        elif depot_section:
            if int(line) == -1:
                continue
            depot = int(line)

    # Tworzymy macierz odległości
    size = len(coords)
    distance_matrix = [[0] * size for _ in range(size)]
    for i in coords:
        for j in coords:
            xi, yi = coords[i]
            xj, yj = coords[j]
            dist = math.hypot(xi - xj, yi - yj)
            distance_matrix[i - 1][j - 1] = dist

    # demands do listy
    demand_list = [0] * size
    for idx in demands:
        demand_list[idx - 1] = demands[idx]

    return distance_matrix, demand_list, capacity
