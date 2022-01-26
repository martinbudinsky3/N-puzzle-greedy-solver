operators_dict = {"U": "UP", "D": "DOWN", "R": "RIGHT", "L": "LEFT"}


class Input:
    def __init__(self, heuristic, width, height, init_state, goal_state):
        self.heuristic = heuristic
        self.width = width
        self.height = height
        self.init_state = init_state
        self.goal_state = goal_state


def read_input(file_path):
    file = open(file_path, "r")

    first_line = file.readline().split()
    heuristic = int(first_line[0])
    width = int(first_line[1])
    height = int(first_line[2])
    file.readline()
    init_state = read_state(file, height)
    file.readline()
    goal_state = read_state(file, height)

    return Input(heuristic, width, height, init_state, goal_state)


def read_state(f, n):
    state = []

    for i in range(n):
        line = f.readline()
        row = line.split()
        state.append(row)

    return state


# function to format and print output
def print_output(result, start, end):
    if result.sequence is None:
        print("Solution does not exist")
        print("Total number of nodes:", result.number_of_nodes)
        print("Time: {} s".format(end - start))
        return

    result_sequence = result.sequence
    init_node = result_sequence.pop(0)
    print_state(init_node.state)

    for node in result_sequence:
        print()
        print(operators_dict[node.last_move])
        print()
        print_state(node.state)

    number_of_ops = len(result_sequence) - 1

    print()
    print("Number of moves:", number_of_ops)
    print("Total number of nodes:", result.number_of_nodes)
    print("Time: {} s".format(end - start))


def print_state(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            print(state[i][j], end=" ")
        print()