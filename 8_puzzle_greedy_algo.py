import math
import heapq
import copy
import time

PRINT = 0

# min heap to store generated nodes, key is heuristic distance estimation
generated_nodes = []
# list to store all processed states to avoid duplicates while generating new states
processed_states = {}
# dictionary to store values:coordinates pairs of goal state
goal_dict = {}


# class representing node
class Node:
    def __init__(self, state, parent, last_move, dist):
        self.state = state
        self.parent = parent
        self.last_move = last_move
        self.dist = dist

    def __lt__(self, other):
        return self.dist < other.dist


# heuristic that returns number of wrong placed tiles
def heuristic1(actual_state, goal_state, m, n):
    wrong_tiles = 0

    for i in range(n):
        for j in range(m):
            if actual_state[i][j] != goal_state[i][j]:
                wrong_tiles += 1

    return wrong_tiles


# heuristic that returns sum of manhattan distances
def heuristic2(actual_state, m, n):
    manhattan_distance = 0

    for i in range(n):
        for j in range(m):
            x_act = j
            y_act = i

            coordinates = goal_dict[actual_state[i][j]]
            x_goal = coordinates[0]
            y_goal = coordinates[1]
            manhattan_distance += (math.fabs(x_goal - x_act) + math.fabs(y_goal - y_act))

    return manhattan_distance


# function that returns x, y coordinates of blank tile
def find_blank(state, m, n):
    for i in range(n):
        for j in range(m):
            if state[i][j] == "m":
                return j, i

    return None


# function that swap tiles
def swap(state, x_blank, y_blank, x_neigh, y_neigh):
    temp = state[y_blank][x_blank]
    state[y_blank][x_blank] = state[y_neigh][x_neigh]
    state[y_neigh][x_neigh] = temp

    return state


# functions that make moves
def move_up(state, m, n):
    x_blank, y_blank = find_blank(state, m, n)
    if y_blank != n - 1:
        new_state = copy.deepcopy(state)
        new_state = swap(new_state, x_blank, y_blank, x_blank, y_blank + 1)
        return new_state

    return None


def move_down(state, m, n):
    x_blank, y_blank = find_blank(state, m, n)
    if y_blank != 0:
        new_state = copy.deepcopy(state)
        new_state = swap(new_state, x_blank, y_blank, x_blank, y_blank - 1)
        return new_state

    return None


def move_right(state, m, n):
    x_blank, y_blank = find_blank(state, m, n)
    if x_blank != 0:
        new_state = copy.deepcopy(state)
        new_state = swap(new_state, x_blank, y_blank, x_blank - 1, y_blank)
        return new_state

    return None


def move_left(state, m, n):
    x_blank, y_blank = find_blank(state, m, n)
    if x_blank != m - 1:
        new_state = copy.deepcopy(state)
        new_state = swap(new_state, x_blank, y_blank, x_blank + 1, y_blank)
        return new_state

    return None


# function that return estimated distance based on input heuristic
def choose_heuristic(state, goal_state, m, n, heur):
    dist = 0
    if heur == 1:
        dist = heuristic1(state, goal_state, m, n)
    elif heur == 2:
        dist = heuristic2(state, m, n)

    return dist


# function that create node and push it to heap of generated nodes
def create_node(state, goal_state, m, n, parent, last_move, heur):
    dist = choose_heuristic(state, goal_state, m, n, heur)
    node = Node(state, parent, last_move, dist)

    heapq.heappush(generated_nodes, node)


# function that generates all possible new nodes
def generate_nodes(node, goal_state, m, n, heur):
    state = node.state
    last_move = node.last_move

    # generating new states
    up_state = move_up(state, m, n)
    down_state = move_down(state, m, n)
    right_state = move_right(state, m, n)
    left_state = move_left(state, m, n)

    if not processed_states.get(str(up_state), False) and up_state is not None and last_move != "D":
        create_node(up_state, goal_state, m, n, node, "U", heur)

    if not processed_states.get(str(down_state), False) and down_state is not None and last_move != "U":
        create_node(down_state, goal_state, m, n, node, "D", heur)

    if not processed_states.get(str(right_state), False) and right_state is not None and last_move != "L":
        create_node(right_state, goal_state, m, n, node, "R", heur)

    if not processed_states.get(str(left_state), False) and left_state is not None and last_move != "R":
        create_node(left_state, goal_state, m, n, node, "L", heur)


# implementation of greedy algorithm
def greedy(init_state, goal_state, m, n, heur):
    create_node(init_state, goal_state, m, n, None, None, heur)  # creating first init node, creating a min heap
    while generated_nodes:
        if PRINT:
            print("Generated nodes:", len(generated_nodes))
            print("Processed nodes:", len(processed_states.keys()))
            print()

        actual_node = heapq.heappop(generated_nodes)  # extracting min node from heap
        actual_state = actual_node.state
        processed_states[str(actual_state)] = True  # storing state as processed

        if actual_state == goal_state:  # if goal_state was found function returns node with goal state
            return actual_node

        generate_nodes(actual_node, goal_state, m, n, heur)  # generating all possible succesors

    return None  # if algorithm didn't find goal solution function returns None


# functions to read and process input
def create_goal_state_dict(goal_state, m, n):
    for i in range(n):
        for j in range(m):
            tile = goal_state[i][j]
            goal_dict[tile] = (j, i)


def read_state(f, n):
    state = []

    for i in range(n):
        line = f.readline()
        row = line.split()
        state.append(row)

    return state


def read_input(file):
    f = open(file, "r")

    first_line = f.readline()
    heur = int(first_line[0])
    m = int(first_line[2])
    n = int(first_line[4])

    init_state = read_state(f, n)
    f.readline()
    goal_state = read_state(f, n)

    return heur, m, n, init_state, goal_state


# function to format and print output
def print_output(result_node, start, end):
    if result_node is None:
        print("Solution does not exist")
        print("Total number of nodes:", len(processed_states.keys()))
        print("Time: {} s".format(end - start))
        return

    op_dict = {"U": "UP", "D": "DOWN", "R": "RIGHT", "L": "LEFT"}

    number_of_ops = 0
    operators = []
    actual_node = result_node
    while actual_node.parent:
        operators.append(actual_node.last_move)
        actual_node = actual_node.parent
        number_of_ops += 1

    for i in range(len(operators) - 1, -1, -1):
        print(op_dict[operators[i]])

    print()
    print("Number of moves:", number_of_ops)
    print("Total number of nodes:", len(generated_nodes) + len(processed_states.keys()))
    print("Time: {} s".format(end - start))


start = time.perf_counter()
heur, m, n , init_state, goal_state = read_input("basic.txt")
# heur, m, n , init_state, goal_state = read_input("basic_1.txt")
# heur, m, n , init_state, goal_state = read_input("input_3x2.txt")
# heur, m, n , init_state, goal_state = read_input("input_4x2.txt")
# heur, m, n , init_state, goal_state = read_input("input_4x3.txt")
# heur, m, n , init_state, goal_state = read_input("input_5x2.txt")

create_goal_state_dict(goal_state, m, n)
result_node = greedy(init_state, goal_state, m, n, heur)
end = time.perf_counter()
print_output(result_node, start, end)




