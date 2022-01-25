import heapq
import copy
import math

PRINT = 0
BLANK_TILE = "m"


class Result:
    def __init__(self, result_node, generated_nodes, processed_nodes):
        self.result_node = result_node
        self.number_of_nodes = len(generated_nodes) + len(processed_nodes.keys())


# class representing node
class Node:
    def __init__(self, state, parent, last_move, dist):
        self.state = state
        self.parent = parent
        self.last_move = last_move
        self.dist = dist

    def __lt__(self, other):
        return self.dist < other.dist


class GreedySolver:
    def __init__(self, input):
        self.heuristic = input.heuristic
        self.height = input.height
        self.width = input.width
        self.init_state = input.init_state
        self.goal_state = input.goal_state

        # min heap to store generated nodes, key is heuristic distance estimation
        self.generated_nodes = []

        # list to store all processed states to avoid duplicates while generating new states
        self.processed_states = {}

        # dictionary to store values:coordinates pairs of goal state
        self.goal_dict = {}

        self.create_goal_state_dict()

    def create_goal_state_dict(self):
        for i in range(self.height):
            for j in range(self.width):
                tile = self.goal_state[i][j]
                self.goal_dict[tile] = (j, i)

    # implementation of greedy algorithm
    def solve(self):
        self.create_node(self.init_state, None, None)  # creating first init node, creating a min heap
        while self.generated_nodes:
            if PRINT:
                print("Generated nodes:", len(self.generated_nodes))
                print("Processed nodes:", len(self.processed_states.keys()))
                print()

            actual_node = heapq.heappop(self.generated_nodes)  # extracting min node from heap
            actual_state = actual_node.state
            self.processed_states[str(actual_state)] = True  # storing state as processed

            if actual_state == self.goal_state:  # if goal_state was found function returns node with goal state
                return Result(actual_node, self.generated_nodes, self.processed_states)

            self.generate_nodes(actual_node)  # generating all possible succesors

        # if algorithm didn't find goal solution function returns None
        return Result(None, self.generated_nodes, self.processed_states)

    # function that generates all possible new nodes
    def generate_nodes(self, node):
        state = node.state
        last_move = node.last_move

        # generating new states
        up_state = self.move_up(state)
        down_state = self.move_down(state)
        right_state = self.move_right(state)
        left_state = self.move_left(state)

        if not self.processed_states.get(str(up_state), False) and up_state is not None and last_move != "D":
            self.create_node(up_state, node, "U")

        if not self.processed_states.get(str(down_state), False) and down_state is not None and last_move != "U":
            self.create_node(down_state, node, "D")

        if not self.processed_states.get(str(right_state), False) and right_state is not None and last_move != "L":
            self.create_node(right_state, node, "R")

        if not self.processed_states.get(str(left_state), False) and left_state is not None and last_move != "R":
            self.create_node(left_state, node, "L")

    # functions that make moves
    def move_up(self, state):
        x_blank, y_blank = self.find_blank(state)
        if y_blank != self.height - 1:
            new_state = copy.deepcopy(state)
            new_state = self.swap(new_state, x_blank, y_blank, x_blank, y_blank + 1)
            return new_state

        return None

    def move_down(self, state):
        x_blank, y_blank = self.find_blank(state)
        if y_blank != 0:
            new_state = copy.deepcopy(state)
            new_state = self.swap(new_state, x_blank, y_blank, x_blank, y_blank - 1)
            return new_state

        return None

    def move_right(self, state):
        x_blank, y_blank = self.find_blank(state)
        if x_blank != 0:
            new_state = copy.deepcopy(state)
            new_state = self.swap(new_state, x_blank, y_blank, x_blank - 1, y_blank)
            return new_state

        return None

    def move_left(self, state):
        x_blank, y_blank = self.find_blank(state)
        if x_blank != self.width - 1:
            new_state = copy.deepcopy(state)
            new_state = self.swap(new_state, x_blank, y_blank, x_blank + 1, y_blank)
            return new_state

        return None

    # function that returns x, y coordinates of blank tile
    def find_blank(self, state):
        for i in range(self.height):
            for j in range(self.width):
                if state[i][j] == BLANK_TILE:
                    return j, i

        return None

    # function that swap tiles
    def swap(self, state, x_blank, y_blank, x_neighbor, y_neighbor):
        temp = state[y_blank][x_blank]
        state[y_blank][x_blank] = state[y_neighbor][x_neighbor]
        state[y_neighbor][x_neighbor] = temp

        return state

    # function that create node and push it to heap of generated nodes
    def create_node(self, state, parent, last_move):
        dist = self.count_heuristic(state)
        node = Node(state, parent, last_move, dist)

        heapq.heappush(self.generated_nodes, node)

    # function that return estimated distance based on input heuristic
    def count_heuristic(self, state):
        dist = 0
        if self.heuristic == 1:
            dist = self.misplaced_count_heuristic(state)
        elif self.heuristic == 2:
            dist = self.manhattan_heuristic(state)

        return dist

    # heuristic that returns number of wrong placed tiles
    def misplaced_count_heuristic(self, actual_state):
        wrong_tiles = 0

        for i in range(self.height):
            for j in range(self.width):
                if actual_state[i][j] != self.goal_state[i][j]:
                    wrong_tiles += 1

        return wrong_tiles

    # heuristic that returns sum of manhattan distances
    def manhattan_heuristic(self, actual_state):
        manhattan_distance = 0

        for i in range(self.height):
            for j in range(self.width):
                x_act = j
                y_act = i

                coordinates_goal = self.goal_dict[actual_state[i][j]]
                x_goal = coordinates_goal[0]
                y_goal = coordinates_goal[1]
                manhattan_distance += (math.fabs(x_goal - x_act) + math.fabs(y_goal - y_act))

        return manhattan_distance
