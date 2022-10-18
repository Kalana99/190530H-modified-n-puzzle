import random


START_CONF_FILE_NAME = ""
GOAL_CONF_FILE_NAME = ""
OUT_FILE_NAME = ""

START_CONFIG = []
GOAL_CONFIG = []

SIZE = 0

OPENED_STATES = []
CLOSED_STATES = []

PATH = []

H_METHOD = ""  # change this to the preferred method accordingly

MIS_TILE_MOVES = []
MANHATTAN_MOVES = []


def total_misplaced_tiles(config):

    count = 0

    for r in range(SIZE):
        for c in range(SIZE):

            if config[r][c] != GOAL_CONFIG[r][c]:
                count += 1

    return count


def total_manhattan_distance(config):

    total = 0

    for r in range(SIZE):
        for c in range(SIZE):

            tile = config[r][c]

            if tile != '-':

                for r2 in range(SIZE):
                    for c2 in range(SIZE):

                        if GOAL_CONFIG[r2][c2] == tile:
                            total += abs(r2 - r) + abs(c2 - c)

    return total


class State:

    def __init__(self, config, parent, g_val):

        self.config = config
        self.parent = parent
        self.g_val = g_val

        self.h_val = State.calc_h(self.config)

    def get_f(self):
        return self.g_val + self.h_val

    @staticmethod
    def calc_h(config):

        if H_METHOD == "miss_tile":
            return total_misplaced_tiles(config)
        else:
            return total_manhattan_distance(config)


# returns the state with the minimum f value in the opened list
def get_minimum_f_state():

    selected_state = OPENED_STATES[0]

    for state in OPENED_STATES:

        if state.get_f() < selected_state.get_f():
            selected_state = state

    return selected_state


# return indices of the blank tiles
def get_blank_tiles(config: []):

    blank_tiles = []

    for row in range(SIZE):
        for col in range(SIZE):

            if config[row][col] == '-':
                if len(blank_tiles) < 2:
                    blank_tiles.append((row, col))

    return blank_tiles


# returns True if the provided (row, col) is in the config limits
def is_in_limits(pos):

    for ind in pos:

        if ind < 0 or ind > SIZE - 1:
            return False

    return True


# return every possible state from a given state
def get_adj_states(curr_state: State):

    blank_tiles = get_blank_tiles(curr_state.config)

    states = []

    for blank_tile in blank_tiles:

        pos1 = (blank_tile[0] - 1, blank_tile[1])
        pos2 = (blank_tile[0] + 1, blank_tile[1])
        pos3 = (blank_tile[0], blank_tile[1] - 1)
        pos4 = (blank_tile[0], blank_tile[1] + 1)

        new_positions = [pos1, pos2, pos3, pos4]

        for pos in new_positions:

            temp_config = [x[:] for x in curr_state.config]

            if is_in_limits(pos):

                temp_config[pos[0]][pos[1]], temp_config[blank_tile[0]][blank_tile[1]] = temp_config[blank_tile[0]][blank_tile[1]], temp_config[pos[0]][pos[1]]
                states.append(State(temp_config, curr_state, curr_state.g_val + 1))

    return states


# returns a start configuration given a size
def get_start_puzzle(size):

    chars = ['-', '-']
    for j in range(size * size - 2):
        chars.append(j + 1)

    puzzle = []
    used_chars = []

    for rows in range(size):

        row = []

        while len(row) < size:

            rand_ind = random.randint(0, len(chars) - 1)
            selected_char = str(chars[rand_ind])

            if selected_char == '-' and used_chars.count('-') < 2:

                row.append(selected_char)
                used_chars.append(selected_char)

            elif selected_char not in used_chars:

                row.append(selected_char)
                used_chars.append(selected_char)

        puzzle.append(row)

    return puzzle


# returns a goal configuration based on the start configuration
def get_goal_puzzle(start_puzzle):

    goal_puzzle = [x[:] for x in start_puzzle]

    move_limit = random.randint(1, 5)
    moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    move_count = 0

    while move_count < move_limit:

        blank_tiles = get_blank_tiles(goal_puzzle)
        moving_blank_tile = random.choice(blank_tiles)

        move = random.choice(moves)

        pos = (moving_blank_tile[0] + move[0], moving_blank_tile[1] + move[1])

        if is_in_limits(pos):

            goal_puzzle[pos[0]][pos[1]], goal_puzzle[moving_blank_tile[0]][moving_blank_tile[1]] = goal_puzzle[moving_blank_tile[0]][moving_blank_tile[1]], goal_puzzle[pos[0]][pos[1]]
            move_count += 1

    return goal_puzzle


# return if state is in opened
def is_opened(state: State):

    for op_state in OPENED_STATES:

        if op_state.config == state.config:
            return True
    return False


# return the instance that matches the state in opened
def get_opened_state(state: State):

    for op_state in OPENED_STATES:

        if op_state.config == state.config:
            return op_state


# return if state is in closed
def is_closed(state: State):

    for cl_state in CLOSED_STATES:

        if cl_state.config == state.config:
            return True
    return False


# return the instance that matches the state in closed
def get_closed_state(state: State):

    for cl_state in CLOSED_STATES:

        if cl_state.config == state.config:
            return cl_state


# format the moves to a string of type (tile, direction)
def format_move(from_state, to_state):

    move = "("

    for row in range(SIZE):
        for col in range(SIZE):

            if from_state.config[row][col] != to_state.config[row][col] and from_state.config[row][col] != '-':

                move += from_state.config[row][col] + ","

                if row - 1 >= 0 and from_state.config[row][col] == to_state.config[row - 1][col]:
                    move += "up)"

                if row + 1 <= (SIZE - 1) and from_state.config[row][col] == to_state.config[row + 1][col]:
                    move += "down)"

                if col - 1 >= 0 and from_state.config[row][col] == to_state.config[row][col - 1]:
                    move += "left)"

                if col + 1 <= (SIZE - 1) and from_state.config[row][col] == to_state.config[row][col + 1]:
                    move += "right)"

                break
    return move


# return the path to goal config
def get_path(curr_state: State):

    path = []

    while curr_state.parent is not None:

        path.append(format_move(curr_state.parent, curr_state))
        curr_state = curr_state.parent

    path.reverse()
    return path


# A* search
def a_star():

    global START_CONFIG, GOAL_CONFIG, OUT_FILE_NAME, SIZE, PATH

    move_count = 0

    while len(OPENED_STATES) > 0:

        current_state = get_minimum_f_state()
        move_count += 1

        if current_state.config == GOAL_CONFIG:

            if H_METHOD == "miss_tile":
                MIS_TILE_MOVES.append(move_count)
            else:
                MANHATTAN_MOVES.append(move_count)

            move_count = 0

            return get_path(current_state)

        OPENED_STATES.remove(current_state)
        CLOSED_STATES.append(current_state)

        adj_states = get_adj_states(current_state)

        for adj_state in adj_states:

            # if adj state is in closed -> compare f -> if less: update and add to the open
            if is_closed(adj_state):

                closed_adj_state = get_closed_state(adj_state)

                if adj_state.get_f() < closed_adj_state.get_f():

                    closed_adj_state.g_val = adj_state.g_val
                    closed_adj_state.parent = adj_state.parent

                    CLOSED_STATES.remove(closed_adj_state)
                    OPENED_STATES.append(closed_adj_state)

            # if adj state in open -> compare f -> if less: update
            elif is_opened(adj_state):

                opened_adj_state = get_opened_state(adj_state)

                if adj_state.get_f() < opened_adj_state.get_f():

                    opened_adj_state.g_val = adj_state.g_val
                    opened_adj_state.parent = adj_state.parent

            # else add adj state to the open
            else:
                OPENED_STATES.append(adj_state)


def empty_global_var():

    global OPENED_STATES, CLOSED_STATES, PATH

    OPENED_STATES = []
    CLOSED_STATES = []

    PATH = []


def final_out(out_type):

    global START_CONFIG, GOAL_CONFIG, OUT_FILE_NAME, SIZE, PATH

    # add starting configuration to the opened list as the initial state
    opening_state = State(START_CONFIG, None, 0)
    OPENED_STATES.append(opening_state)

    PATH = a_star()  # TODO: optimize/set timeout

    if out_type == "1":
        return True
    else:

        OUT_FILE_NAME = "out.txt"

        # write to output file
        f_out = open(OUT_FILE_NAME, "w")
        f_out.write(", ".join(PATH))
        f_out.close()


user_in = input("Enter 1 for analytics and 2 to run sample tests: \n")

if user_in == "1":

    n = int(input("No of tests: "))
    lower_limit = int(input("Puzzle SIZE lower limit(>3): "))
    greater_limit = int(input("Puzzle SIZE greater limit(>3 and >lower limit): "))

    if n < 1 or lower_limit < 3 or greater_limit < lower_limit:
        print("invalid limits")
        exit(-1)

    for p in range(n):

        size = random.randint(lower_limit, greater_limit)

        START_CONFIG = get_start_puzzle(size)
        SIZE = len(START_CONFIG)
        GOAL_CONFIG = get_goal_puzzle(START_CONFIG)

        H_METHOD = "miss_tile"

        final_out(user_in)
        empty_global_var()

        H_METHOD = "manhattan"

        final_out(user_in)
        empty_global_var()

    print(len(MIS_TILE_MOVES), len(MANHATTAN_MOVES))
    print("Misplaced tile moves " + repr(MIS_TILE_MOVES))
    print("Manhattan moves " + repr(MANHATTAN_MOVES))

elif user_in == "2":

    # START_CONF_FILE_NAME = input("Start config file name: ")
    # GOAL_CONF_FILE_NAME = input("Goal config file name: ")

    START_CONF_FILE_NAME = "Sample_Start_Configuration.txt"
    GOAL_CONF_FILE_NAME = "Sample_Goal_Configuration.txt"

    # START_CONF_FILE_NAME = "Start_Configuration_1.txt"
    # GOAL_CONF_FILE_NAME = "Goal_Configuration_1.txt"

    file_start = open(START_CONF_FILE_NAME, "r")
    s_lines = file_start.readlines()

    for line in s_lines:
        START_CONFIG.append(line.strip().split())

    file_start.close()

    file_goal = open(GOAL_CONF_FILE_NAME, "r")
    g_lines = file_goal.readlines()

    for line in g_lines:
        GOAL_CONFIG.append(line.strip().split())

    file_goal.close()

    SIZE = len(START_CONFIG)

    final_out(user_in)
    # empty_global_var()
    #
    # H_METHOD = "manhattan"
    #
    # final_out(user_in)
    # empty_global_var()
    #
    # print("Misplaced tile moves " + repr(MIS_TILE_MOVES))
    # print("Manhattan moves " + repr(MANHATTAN_MOVES))

else:

    print("Invalid Input")
    exit(-1)
