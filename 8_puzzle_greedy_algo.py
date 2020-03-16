import math
import heapq
import copy

generated_nodes = []
processed_states = []


class Node:
    def __init__(self, state, parent, last_move, dist):
        self.state = state
        self.parent = parent
        self.last_move = last_move
        self.dist = dist

    def __lt__(self, other):
        return self.dist < other.dist

def heuristic1(actual_state, goal_state, m, n):
    wrong_tiles = 0

    for i in range(n):
        for j in range(m):
            if actual_state[i][j] != goal_state[i][j]:
                wrong_tiles += 1

    return wrong_tiles


def heuristic2(actual_state, goal_dict, m, n):
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


def find_blank(state, m, n):
    for i in range(n):
        for j in range(m):
            if state[i][j] == "m":
                return j, i

    return None


def swap(state, x_blank, y_blank, x_neigh, y_neigh):
    temp = state[y_blank][x_blank]
    state[y_blank][x_blank] = state[y_neigh][x_neigh]
    state[y_neigh][x_neigh] = temp

    return state


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


def choose_heuristic(heur):
    dist = 0
    if heur == 1:
        dist = heuristic1(init_state, goal_state, m, n)
    elif heur == 2:
        dist = heuristic2(init_state, goal_state, m, n)

    return dist


def create_node(state, parent, last_move, heur):
    dist = choose_heuristic(heur)
    node = Node(state, parent, last_move, dist)

    heapq.heappush(generated_nodes, (dist, node))


def generate_nodes(node, m, n, heur):
    state = node.state
    last_move = node.last_move

    up_state = move_up(state, m, n)
    down_state = move_down(state, m, n)
    right_state = move_right(state, m, n)
    left_state = move_left(state, m, n)

    if up_state not in processed_states and up_state is not None and last_move != "D":
        create_node(up_state, node, "U", heur)

    if down_state not in processed_states and down_state is not None and last_move != "U":
        create_node(down_state, node, "D", heur)

    if right_state not in processed_states and right_state is not None and last_move != "L":
        create_node(right_state, node, "R", heur)

    if left_state not in processed_states and left_state is not None and last_move != "R":
        create_node(left_state, node, "L", heur)


def greedy(init_state, goal_state, m, n, heur):
    create_node(init_state, None, None, heur)
    while generated_nodes != []:
        dist_node = heapq.heappop(generated_nodes)
        actual_node = dist_node[1]
        actual_state = actual_node.state
        if actual_state == goal_state:
            return actual_node;
        generate_nodes(actual_node, m, n, heur)
        processed_states.append(actual_state)

    return None


def create_goal_state_dict(goal_state, m, n):
    goal_dict = {}

    for i in range(n):
        for j in range(m):
            tile = goal_state[i][j]
            goal_dict[tile] = (j, i)

    return goal_dict


def read_state(f, m, n):
    state = []
    row = []

    for i in range(n):
        line = f.readline()
        for j in range(m):
            row.append(line[j * 2])
        state.append(row)
        row = []

    return state


def read_input(file):
    f = open(file, "r")

    first_line = f.readline()
    heur = int(first_line[0])
    m = int(first_line[2])
    n = int(first_line[4])

    init_state = read_state(f, m, n)
    f.readline()
    goal_state = read_state(f, m, n)

    return heur, m, n, init_state, goal_state


heur, m, n , init_state, goal_state = read_input("input.txt")
goal_dict = create_goal_state_dict(goal_state, m, n)
result = greedy(init_state, goal_state, m, n, heur)

print(result.state)
# print(init_state)
# print(final_state)



