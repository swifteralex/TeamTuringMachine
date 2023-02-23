import copy


class Container:
    def __init__(self, name, weight, sifted=False):
        self.name = name
        self.weight = weight
        self.sifted = sifted


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
        return __sift(state)
        # for key in state.containers:
        #     print(str(key) + " " + str(state.containers[key].weight))

    print("Balancing!")


def load_unload(state):
    print("Loading/unloading!")


def __sift(state):
    move_set = []

    # Sort all containers by weight
    weights = []
    for key in state.containers:
        weights.append(state.containers[key].weight)
    weights.sort()

    # Get destination coordinates for each weight
    destinations = []
    count = 0
    coord = (1, 6)
    while count < len(weights):
        while not state.ship[coord[0]][6]:
            coord = (coord[0] + 1, coord[1])
        while coord[1] >= 0 and state.ship[coord[0]][coord[1]]:
            destinations.append((coord[0], coord[1]))
            count += 1
            if count == len(weights):
                break
            destinations.append((coord[0], 13 - coord[1]))
            count += 1
            if count == len(weights):
                break
            coord = (coord[0], coord[1] - 1)
        coord = (coord[0] + 1, 6)
    destinations.reverse()

    while weights:
        target_weight = weights.pop()
        destination = destinations.pop()

        # Check if container is already where it needs to be
        if destination in state.containers and state.containers[destination].weight == target_weight:
            state.containers[destination].sifted = True
            continue

        # If not, find its current coordinates. If duplicates exist, find one with the least containers above it
        target_coords = []
        for key in state.containers:
            if state.containers[key].weight == target_weight and not state.containers[key].sifted:
                target_coords.append(key)
        least_stacks = 99
        best_target = target_coords[0]
        for target in target_coords:
            current_stack = 0
            coord_pointer = target
            while coord_pointer in state.containers:
                current_stack += 1
                coord_pointer = (coord_pointer[0] + 1, coord_pointer[1])
            if current_stack < least_stacks:
                best_target = target
                least_stacks = current_stack

        # For each container above it, move that container to
        #   1. the closest spot that isn't in the destination column or the best_target column
        #      (prefer putting heavier weights on top of lighter weights)
        #   2. if that isn't possible, the buffer
        __free_coord(
            state, best_target, move_set, best_target, weights, destinations, [destination[1], best_target[1]]
        )

        # For each container in the destination column, move it to
        #   1. the closest spot that isn't in the destination column or the best_target column
        #      (prefer putting heavier weights on top of lighter weights)
        #   2. if that isn't possible, the buffer
        best_target = __free_coord(
            state, (destination[0] - 1, destination[1]), move_set, best_target, weights, destinations,
            [destination[1], best_target[1]]
        )

        # Find best route to destination spot
        moves = __interpolate(state, best_target, destination)
        move_set.append(moves)
        container_to_move = state.containers.pop(best_target)
        container_to_move.sifted = True
        state.containers[moves[-1]] = container_to_move

    return move_set


def __get_moves(state, excluded_columns):
    moves = []
    for i in range(1, 13):
        if excluded_columns.count(i) > 0:
            continue
        coord = (1, i)
        while coord[0] <= 8 and (coord in state.containers or not state.ship[coord[0]][coord[1]]):
            coord = (coord[0] + 1, i)
        if coord[0] <= 8:
            moves.append(coord)

    coord = (-1, -24)
    while coord in state.containers:
        coord = (coord[0], coord[1] + 1)
    moves.append(coord)

    return moves


def __interpolate(state, start, end):
    if start[0] < 0 and end[0] > 0:
        return __interpolate(state, start, (-5, -24)) + __interpolate(state, (9, 1), end)
    if start[0] > 0 and end[0] < 0:
        return __interpolate(state, start, (9, 1)) + __interpolate(state, (-5, -24), end)

    moves = [start]
    coord = start

    if coord[1] < end[1]:
        step = 1
    else:
        step = -1

    while coord[1] < end[1] or coord[1] > end[1]:
        while coord[0] <= 8 and ((coord[0], coord[1] + step) in state.containers
                                 or (start[0] > 0 and not state.ship[coord[0]][coord[1] + step])):
            if start[0] > 0:
                coord = (coord[0] + 1, coord[1])
            else:
                coord = (coord[0] - 1, coord[1])
            moves.append(coord)
        coord = (coord[0], coord[1] + step)
        moves.append(coord)

    while coord[0] > end[0]:
        coord = (coord[0] - 1, coord[1])
        moves.append(coord)
    while coord[0] < end[0] < 0:
        coord = (coord[0] + 1, coord[1])
        moves.append(coord)

    return moves


def __free_coord(state, coord_to_free, move_set, target, weights, destinations, excluded_columns=None):
    if excluded_columns is None:
        excluded_columns = []

    while (coord_to_free[0] + 1, coord_to_free[1]) in state.containers:
        coord = (8, coord_to_free[1])
        while coord not in state.containers:
            coord = (coord[0] - 1, coord_to_free[1])
        top_container_weight = state.containers[coord].weight

        moves = __get_moves(state, excluded_columns)

        ideal_moves = []
        ideal_column_moves = []
        lighter_on_heavier_columns = []
        buffer_moves = []
        for move in moves:
            try:
                if move == destinations[weights.index(top_container_weight)]:
                    ideal_column_moves.clear()
                    ideal_column_moves.append(move)
                    break
            except ValueError:
                pass

            if move[0] < 0:
                buffer_moves.append(move)
            elif (move[0] - 1, move[1]) not in state.containers:
                ideal_column_moves.append(move)
            else:
                if state.containers[(move[0] - 1, move[1])].sifted:
                    ideal_column_moves.append(move)
                elif state.containers[(move[0] - 1, move[1])].weight <= top_container_weight:
                    ideal_column_moves.append(move)
                else:
                    lighter_on_heavier_columns.append(move)

        if not ideal_column_moves and not lighter_on_heavier_columns:
            ideal_moves = __interpolate(state, coord, buffer_moves[0])
        else:
            if not ideal_column_moves:
                moves = lighter_on_heavier_columns
            else:
                moves = ideal_column_moves
            best_distance = 99
            for move in moves:
                distance = __interpolate(state, coord, move)
                if len(distance) < best_distance:
                    ideal_moves = distance
                    best_distance = len(distance)
        move_set.append(ideal_moves)
        container_to_move = state.containers.pop(coord)
        state.containers[ideal_moves[-1]] = container_to_move
        if ideal_moves[0] == target:
            excluded_columns.append(ideal_moves[-1][1])
            target = ideal_moves[-1]
    return target
