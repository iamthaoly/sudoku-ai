from itertools import product

def convert_to_set(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution=[]):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j: X[k].remove(i)
        cols.append(X.pop(j))
    return cols 

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k!= j:
                    X[k].add(i)

def solve_sudoku_X(size, grid):
    row, col = size
    # calculate total squares in grid 
    N = row * col
    X = ([("rc", rc) for rc in product(range(N), range(N))] + 
        [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
        [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
        [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // row) * row + (c // col) # box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]

    X, Y = convert_to_set(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n: select(X, Y, (i, j, n))

    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n 
        yield grid

if __name__ == "__main__":
    size = (3, 3)
    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0], \
        [6, 0, 0, 1, 9, 5, 0, 0, 0], \
        [0, 9, 8, 0, 0, 0, 0, 6, 0], \
        [8, 0, 0, 0, 6, 0, 0, 0, 3], \
        [4, 0, 0, 8, 0, 3, 0, 0, 1], \
        [7, 0, 0, 0, 2, 0, 0, 0, 6], \
        [0, 6, 0, 0, 0, 0, 2, 8, 0], \
        [0, 0, 0, 4, 1, 9, 0, 0, 5], \
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    solution = solve_sudoku_X(size, grid)
    solution = list(solution)
    print(solution[0])