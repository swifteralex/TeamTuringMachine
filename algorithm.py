import itertools

class Container:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


class State:
    def __init__(self, ship, containers):
        # 8x12 bool array showing which grid cells are NAN -- False is NAN, True is empty
        # The array is 1 unit wider and longer so that indices start at 1, following the manifest's coord. convention
        self.ship = ship

        # Dictionary of containers -- each container is indexed by a tuple of its coordinates as shown on the manifest
        # Buffer coordinates have negative values as a convention
        self.containers = containers


def __have_to_sift(state):
    weights = []
    total_weight = 0
    for key in state.containers:
        weights.append(state.containers[key].weight)
        total_weight += state.containers[key].weight

    # Get all subsets to see if any of them satisfy the legal definition of balancing
    n = len(weights)
    for i in range(2 ** n):
        subset = []
        left_side_weight = 0
        for j in range(n):
            if i & (1 << j):
                subset.append(weights[j])
                left_side_weight += weights[j]
        if total_weight - left_side_weight > left_side_weight:
            bigger_weight = total_weight - left_side_weight
            smaller_weight = left_side_weight
        else:
            bigger_weight = left_side_weight
            smaller_weight = total_weight - left_side_weight
        if bigger_weight * 0.9 <= smaller_weight and smaller_weight * 1.1 >= bigger_weight:
            return False
    return True


def read_manifest(filepath):  # Takes in a manifest file and returns a State object
    manifest = open(filepath, 'r')
    containers = {}
    ship = [None]
    for i in range(0, 8):
        new_row = [None]
        for j in range(0, 12):
            line = manifest.readline()
            name = line[18:].strip()
            if name != "NAN":
                if name != "UNUSED":
                    coord_tuple = (i + 1, j + 1)
                    weight = int(line[10:15])
                    containers[coord_tuple] = Container(name, weight)
                new_row.append(True)
            else:
                new_row.append(False)
        ship.append(new_row)
    return State(ship, containers)


def balance(manifest):
    state = read_manifest(manifest)
    if __have_to_sift(state):
        return __sift()

    print("Balancing!")


def load_unload(state):
    print("Loading/unloading!")


def __sift():
    print("Sifting!")
