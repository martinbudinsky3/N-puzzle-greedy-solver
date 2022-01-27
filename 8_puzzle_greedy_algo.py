import time
from ui import read_input, print_output, should_exit
from solver import GreedySolver


while True:
    input = read_input()
    greedy_solver = GreedySolver(input)

    start = time.perf_counter()
    result = greedy_solver.solve()
    end = time.perf_counter()

    print_output(result, start, end)

    if should_exit():
        break
