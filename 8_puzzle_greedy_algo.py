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
    m = int(first_line[0])
    n = int(first_line[2])

    init_state = read_state(f, m, n)
    f.readline()
    final_state = read_state(f, m, n)

    return m, n, init_state, final_state


m, n , init_state, final_state = read_input("input.txt")
print(init_state)
print(final_state)



