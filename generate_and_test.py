import random
import modified_n_puzzle


def generate_start_states(size):
    """generate a start configuration"""
    tiles = [i for i in range(1, size ** 2 - 1)] + ["-", "-"]
    random.shuffle(tiles)

    return tiles


def move_up(state, size, coordinates):
    new_state = state.copy()
    if coordinates[0] <= 0:
        return new_state
    else:
        i = size * coordinates[0] + coordinates[1]
        j = size * (coordinates[0] - 1) + coordinates[1]

        (new_state[i], new_state[j]) = (new_state[j], new_state[i])
        return new_state


def move_down(state, size, coordinates):
    new_state = state.copy()
    if coordinates[0] >= size:
        return new_state
    else:
        i = size * coordinates[0] + coordinates[1]
        j = size * (coordinates[0] + 1) + coordinates[1]

        (new_state[i], new_state[j]) = (new_state[j], new_state[i])
        return new_state


def move_left(state, size, coordinates):
    new_state = state.copy()
    if coordinates[0] % size == 0:
        return new_state
    else:
        i = size * coordinates[0] + coordinates[1]
        j = i - 1

        (new_state[i], new_state[j]) = (new_state[j], new_state[i])
        return new_state


def move_right(state, size, coordinates):
    new_state = state.copy()
    if coordinates[0] % size == size - 1:
        return new_state
    else:
        i = size * coordinates[0] + coordinates[1]
        j = i + 1

        (new_state[i], new_state[j]) = (new_state[j], new_state[i])
        return new_state


def move_random(state, size):
    moving_tiles = [i for i, e in enumerate(state) if e == "-"]
    tile_to_move = moving_tiles[random.randint(0, 1)]
    coordinates = (tile_to_move // size, tile_to_move % size)

    move = [
        lambda: move_up(state, size, coordinates),
        lambda: move_down(state, size, coordinates),
        lambda: move_left(state, size, coordinates),
        lambda: move_right(state, size, coordinates),
    ][random.randint(0, 3)]

    try:
        return move()
    except:
        return state


def generate_goal(state, size, n):
    """generate a goal state with n random moves"""
    goal = state.copy()
    for _ in range(n):
        goal = move_random(goal, size)

    return goal


def run(size, moves=10):
    start = generate_start_states(size)
    goal = generate_goal(start, size, moves)

    puzzle1 = modified_n_puzzle.ModifiedNPuzzle(
        start,
        goal,
        "manhattan"
    )
    puzzle2 = modified_n_puzzle.ModifiedNPuzzle(
        start,
        goal,
        "misplaced"
    )

    return puzzle1.solve(), puzzle2.solve()


if __name__ == "__main__":
    results = []  # contain (manhattan_score, misplaced_score)

    '''
        comparing checks with manhattan vs misplace heuristic functions
        Test plan
        5 x 5 = 50
        6 x 6 - 8 x 8 = 10 for each
        9 x 9 - 10 x 10 = 5 for each
        11 x 11 - 20 x 20 = 1 for each

        total = 100
    '''

    f = lambda i, s: print(f"\033[96m Iteration {i} of size {s}\n \033[0m")
    for _ in range(50):
        f(_, 5)
        results.append(run(5))

    for j in range(6,9):
        for _ in range(10):
            f(_, j)
            results.append(run(j))

    for k in range(9,11):
        for _ in range(5):
            f(_, k)
            results.append(run(k))

    for l in range(11, 21):
        f(1, l)
        results.append(run(l))

    with open("results.txt", 'w') as f:
        for m, n in results:
            f.write(m + " " + n + "\n")
