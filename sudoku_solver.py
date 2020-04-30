import numpy as np
import itertools
import time

# easy sudoku board
grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]


# supposed hardest sudoku board ever!
'''grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]'''

print(np.matrix(grid))

def possible(y, x, n):
    global grid
    for i in range(0,9):
        if grid[y][i] == n :
            return False
    for j in range(0,9):
        if grid[j][x] == n :
            return False
    x0 = (x//3) * 3
    y0 = (y//3) * 3
    for i, j in itertools.product(range(3),range(3)):
        if grid[y0+i][x0+j] == n :
            return False
    return True

def solve():
    global grid
    for x, y in itertools.product(range(9),range(9)):
        if grid[y][x] == 0:
            for n in range(1,10):
                if possible(y,x,n):
                    grid[y][x] = n
                    solve()
                    grid[y][x] = 0
            return
        
    print(np.matrix(grid))
    input('More?')

begin = time.time()
solve()
end = time.time()
print(end-begin)

