import time
from ui import read_input, print_output
from solver import GreedySolver


input = read_input("input_5x2.txt")
greedy_solver = GreedySolver(input)

start = time.perf_counter()
result = greedy_solver.solve()
end = time.perf_counter()

print_output(result, start, end)



