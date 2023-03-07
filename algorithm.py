import copy
import itertools


class Container:
    def __init__(self, name, weight, sifted=False, destination=None):
        self.name = name
        self.weight = weight
        self.sifted = sifted
        self.destination = destination


class State:
    def __init__(self, ship, containers):
        # 8x12 bool array showing which grid cells are NAN -- False is NAN, True is empty
        # The array is 1 unit wider and longer so that indices start at 1, following the manifest's coord. convention
        self.ship = ship

        # Dictionary of containers -- each container is indexed by a tuple of its coordinates as shown on the manifest
        # Buffer coordinates have negative values as a convention
        self.containers = containers


def __get_balanced_arrangements(state):
    arrangements = []

    coords = list(state.containers.keys())
    total_weight = 0
    for key in state.containers:
        total_weight += state.containers[key].weight

    # Calculate available space in the ship. This is important if the ship is especially small
    space = 0
    for i in range(1, 9):
        for j in range(1, 7):
            if state.ship[i][j]:
                space += 1

    # Get all subsets that satisfy the legal definition of balancing
    n = len(coords)
    for i in range(2 ** n):
        subset = []
        left_side_weight = 0
        for j in range(n):
            if i & (1 << j):
                subset.append(coords[j])
                left_side_weight += state.containers[coords[j]].weight
        if total_weight - left_side_weight > left_side_weight:
            bigger_weight = total_weight - left_side_weight
            smaller_weight = left_side_weight
        else:
            bigger_weight = left_side_weight
            smaller_weight = total_weight - left_side_weight
        if bigger_weight * 0.9 <= smaller_weight and smaller_weight * 1.1 >= bigger_weight:
            if len(subset) <= space and len(state.containers) - len(subset) <= space:
                arrangements.append(subset)

    return arrangements


def get_remaining_time(moves, moves_i=0, moves_j=0):
    def __get_time(coord1, coord2):
        if type(coord1) == str or coord1[0] == 0 or coord2[0] == 0:
            return 2
        if coord1[0] > 0 and coord2[1] < 0 or coord1[0] < 0 and coord2[1] > 0:
            return 4
        return 1

    total_time = 0
    offset = True
    for i in range(moves_i, len(moves)):
        for j in range(moves_j if offset else 0, len(moves[i]) - 1):
            total_time += __get_time(moves[i][j], moves[i][j+1])
        offset = False

    return total_time


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
    arrangements = __get_balanced_arrangements(state)

    if not arrangements:
        return __sift(state)

    best_move_set = []
    best_move_set_time = 999

    for arrangement in arrangements:
        state_c = copy.deepcopy(state)
        misplaced_coords = []

        for key in state_c.containers:
            if key in arrangement and key[1] >= 7:
                state_c.containers[key].destination = "left"
                misplaced_coords.append(key)
            elif key not in arrangement and key[1] <= 6:
                state_c.containers[key].destination = "right"
                misplaced_coords.append(key)

        # Search through misplaced coords. If there is a misplaced coord above it, skip it for later.
        # Once a valid misplaced coord is found, free it and move it to the other side. When freeing, don't
        # place containers on top of other misplaced coords, unless the program has to.
        move_set = []
        finished = False
        while not finished:
            finished = True
            coord = []

            if misplaced_coords:
                for remaining_coord in misplaced_coords:
                    if remaining_coord in state_c.containers and not state_c.containers[remaining_coord].sifted:
                        coord = remaining_coord
                        finished = False
                        break
            else:
                for key in state_c.containers:
                    if key[0] < 0:
                        coord = key
                        finished = False
                        break

            if not finished:
                free_to_move = True
                top_coord = (coord[0] + 1, coord[1])
                while top_coord[0] <= 8:
                    if top_coord in misplaced_coords:
                        free_to_move = False
                        misplaced_coords.remove(coord)
                        misplaced_coords.append(coord)
                        break
                    top_coord = (top_coord[0] + 1, top_coord[1])
                if free_to_move or not misplaced_coords:
                    if coord[0] > 0:
                        if coord[1] <= 6:
                            excluded_columns = [coord[1], 7, 8, 9, 10, 11, 12]
                        else:
                            excluded_columns = [coord[1], 1, 2, 3, 4, 5, 6]
                        __free_coord(
                            state_c, coord, move_set, coord, [], misplaced_coords, excluded_columns, "balancing"
                        )

                    if coord[1] >= 7 or (not misplaced_coords and state_c.containers[coord].destination == "left"):
                        excluded_columns = [7, 8, 9, 10, 11, 12]
                    else:
                        excluded_columns = [1, 2, 3, 4, 5, 6]
                    __free_coord(
                        state_c, (coord[0] - 1, coord[1]), move_set, coord, [], misplaced_coords, excluded_columns, "balancing"
                    )

                    if coord[0] > 0:
                        misplaced_coords.remove(coord)
                    if move_set[-1][-1][0] > 0:
                        state_c.containers[move_set[-1][-1]].sifted = True

        total_time = get_remaining_time(move_set)
        if total_time < best_move_set_time:
            best_move_set_time = total_time
            best_move_set = move_set

    return best_move_set


def load_unload(manifest, loads, unloads):
    state = read_manifest(manifest)

    # Get list of all possible unload sequences
    all_unload_orderings = []
    if unloads:
        possible_unloads = []
        for unload in unloads:
            duplicates = []
            for key in state.containers:
                if state.containers[key].weight == state.containers[unload].weight \
                        and state.containers[key].name == state.containers[unload].name:
                    duplicates.append(key)
            possible_unloads.append(duplicates)

        first_unloads = possible_unloads.pop()
        sequences = []
        for unload in first_unloads:
            sequences.append([unload])
        for unload in possible_unloads:
            temp = []
            for coord in unload:
                new_sequences = copy.deepcopy(sequences)
                for sequence in new_sequences:
                    sequence.append(coord)
                temp += new_sequences
            sequences = temp

        for sequence in sequences:
            removed_duplicates = [*set(sequence)]
            if len(removed_duplicates) == len(unloads):
                permuted_orderings = list(__permutations(removed_duplicates))
                for ordering in permuted_orderings:
                    if ordering not in all_unload_orderings:
                        all_unload_orderings.append(ordering)

    valid_unload_orderings = []
    for ordering in all_unload_orderings:
        add_ordering = True
        for i in range(0, len(ordering)):
            for j in range(0, len(ordering)):
                if ordering[i][1] == ordering[j][1] and ordering[i][0] > ordering[j][0] and i < j:
                    add_ordering = False
        if add_ordering:
            valid_unload_orderings.append(ordering)

    best_move_set = []
    best_move_set_distance = 999
    if not valid_unload_orderings:
        valid_unload_orderings.append(None)
    for unloads_c in valid_unload_orderings:
        loads_c = copy.deepcopy(loads)
        move_set = []
        state_c = copy.deepcopy(state)
        empty_buffer = False
        while loads_c or unloads_c or empty_buffer:
            if unloads_c and unloads_c is not None:
                excluded_columns = []
                for coord in unloads_c:
                    excluded_columns.append(coord[1])
                coord = unloads_c.pop()
                __free_coord(state_c, coord, move_set, coord, [], [], excluded_columns, "load_unload")
                moves = __interpolate(state_c, coord, (9, 1))
                beginning_move = ()
                if not move_set:
                    beginning_move = (9, 1)
                else:
                    beginning_move = move_set[-1][-1]
                empty_moves = __interpolate(state_c, beginning_move, moves[0])
                if empty_moves:
                    move_set.append(empty_moves)
                move_set.append(moves)
                move_set[-1].append((0, 0))
                state_c.containers.pop(coord)

            if loads_c:
                excluded_columns = []
                if unloads_c is not None:
                    for coord in unloads_c:
                        excluded_columns.append(coord[1])
                moves = __get_moves(state_c, excluded_columns)
                best_distance = 99
                best_move = []
                for move in moves:
                    if move[0] > 0:
                        interpolated_move = __interpolate(state_c, (9, 1), move)
                        if len(interpolated_move) < best_distance:
                            best_move = interpolated_move
                            best_distance = len(interpolated_move)
                if best_move:
                    loaded_container = loads_c.pop()
                    best_move.insert(0, loaded_container)
                    beginning_move = ()
                    if not move_set:
                        beginning_move = (9, 1)
                    else:
                        beginning_move = move_set[-1][-1]
                    empty_moves = __interpolate(state_c, beginning_move, best_move[0])
                    if empty_moves:
                        move_set.append(empty_moves)
                    move_set.append(best_move)
                    state_c.containers[best_move[-1]] = Container(loaded_container, 0)

            empty_buffer = False
            buffer_cord = ()
            for key in state_c.containers:
                if key[0] < 0:
                    empty_buffer = True
                    buffer_cord = key
                    break
            if (not unloads_c or unloads_c is None) and not loads_c and empty_buffer:
                moves = __get_moves(state_c, [])
                best_distance = 99
                best_move = []
                for move in moves:
                    if move[0] > 0:
                        interpolated_move = __interpolate(state_c, buffer_cord, move)
                        if len(interpolated_move) < best_distance:
                            best_move = interpolated_move
                            best_distance = len(interpolated_move)
                beginning_move = ()
                if not move_set:
                    beginning_move = (9, 1)
                else:
                    beginning_move = move_set[-1][-1]
                empty_moves = __interpolate(state_c, beginning_move, best_move[0])
                if empty_moves:
                    move_set.append(empty_moves)
                move_set.append(best_move)
                container_to_move = state_c.containers.pop(buffer_cord)
                state.containers[best_move[-1]] = container_to_move

        total_time = get_remaining_time(move_set)
        if total_time < best_move_set_distance:
            best_move_set_distance = total_time
            best_move_set = move_set

    return best_move_set


# Credit: this function comes from https://stackoverflow.com/questions/104420/how-do-i-generate-all-permutations-of-a-list
def __permutations(elements):
    if len(elements) <= 1:
        yield elements
        return
    for perm in __permutations(elements[1:]):
        for i in range(len(elements)):
            # nb elements[0:1] works in both string and list contexts
            yield perm[:i] + elements[0:1] + perm[i:]


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
            state, best_target, move_set, best_target, weights, destinations,
            [destination[1], best_target[1]], "sifting"
        )

        # For each container in the destination column, move it to
        #   1. the closest spot that isn't in the destination column or the best_target column
        #      (prefer putting heavier weights on top of lighter weights)
        #   2. if that isn't possible, the buffer
        best_target = __free_coord(
            state, (destination[0] - 1, destination[1]), move_set, best_target, weights, destinations,
            [destination[1], best_target[1]], "sifting"
        )

        # Find best route to destination spot
        moves = __interpolate(state, best_target, destination)
        if not move_set:
            beginning_move = (9, 1)
        else:
            beginning_move = move_set[-1][-1]
        move_set.append(__interpolate(state, beginning_move, moves[0]))
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
    if type(start) is str:
        start = (0, 0)
    if type(end) is str:
        end = (0, 0)

    truck_start = False
    truck_end = False
    if start == (0, 0):
        start = (9, 1)
        truck_start = True
    if end == (0, 0):
        end = (9, 1)
        truck_end = True


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
    while coord[0] < end[0]:
        coord = (coord[0] + 1, coord[1])
        moves.append(coord)

    if truck_start:
        moves.insert(0, (0, 0))
    if truck_end:
        moves.append((0, 0))

    if len(moves) == 1 or moves == [(0, 0), (9, 1), (0, 0)]:
        return []

    return moves


def __free_coord(state, coord_to_free, move_set, target, weights, destinations, excluded_columns, action):
    while (coord_to_free[0] + 1, coord_to_free[1]) in state.containers:
        coord = (8, coord_to_free[1])
        while coord not in state.containers:
            coord = (coord[0] - 1, coord_to_free[1])
        top_container_weight = state.containers[coord].weight

        moves = __get_moves(state, excluded_columns)
        ideal_moves = []
        ideal_column_moves = []
        less_ideal_moves = []
        buffer_moves = []
        for move in moves:
            if action == "sifting":
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
                        less_ideal_moves.append(move)
            elif action == "balancing":
                if move[0] < 0:
                    buffer_moves.append(move)
                elif (move[0] - 1, move[1]) not in state.containers:
                    ideal_column_moves.append(move)
                else:
                    column_contains_misplaced = False
                    top_coord = (0, move[1])
                    while top_coord[0] <= 8:
                        if top_coord in destinations and not state.containers[top_coord].sifted:
                            column_contains_misplaced = True
                            break
                        top_coord = (top_coord[0] + 1, top_coord[1])
                    if not column_contains_misplaced:
                        ideal_column_moves.append(move)
            else:
                if move[0] < 0:
                    buffer_moves.append(move)
                else:
                    ideal_column_moves.append(move)

        if not ideal_column_moves and not less_ideal_moves:
            ideal_moves = __interpolate(state, coord, buffer_moves[0])
            if action == "balancing" and state.containers[coord].destination is None:
                if coord[1] <= 6:
                    state.containers[coord].destination = "left"
                else:
                    state.containers[coord].destination = "right"
        else:
            if not ideal_column_moves:
                moves = less_ideal_moves
            else:
                moves = ideal_column_moves
            best_distance = 99
            for move in moves:
                distance = __interpolate(state, coord, move)
                if len(distance) < best_distance:
                    ideal_moves = distance
                    best_distance = len(distance)
        beginning_move = ()
        if not move_set:
            beginning_move = (9, 1)
        else:
            beginning_move = move_set[-1][-1]
        move_set.append(__interpolate(state, beginning_move, ideal_moves[0]))
        move_set.append(ideal_moves)
        container_to_move = state.containers.pop(coord)
        state.containers[ideal_moves[-1]] = container_to_move
        if ideal_moves[0] == target and not action == "balancing":
            excluded_columns.append(ideal_moves[-1][1])
            target = ideal_moves[-1]
    return target
