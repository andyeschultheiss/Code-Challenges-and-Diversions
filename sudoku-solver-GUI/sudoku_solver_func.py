

# supposed hardest sudoku board ever
'''board = [
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

# easy sudoku board
'''board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
]'''

def checkvalidpuzzle(self, arr):
        subsquarestartingpoints = [[0, 0], [0, 3], [0, 6], [3, 0], [3, 3], [3, 6], [6, 0], [6, 3], [6, 6]]
        # Checking row validity of every row
        for row in range(9):
            has = set()
            for col in range(9):
                if arr[row][col] == 0:
                    continue
                if arr[row][col] in has:
                    return False
                has.add(arr[row][col])
        # Checking column validity of every column
        for col in range(9):
            has = set()
            for row in range(9):
                if arr[row][col] == 0:
                    continue
                if arr[row][col] in has:
                    return False
                has.add(arr[row][col])
        # Checking box validity
        for pointrow, pointcol in subsquarestartingpoints:
            has = set()
            for row in range(3):
                for col in range(3):
                    if arr[pointrow+row][pointcol+col] == 0:
                        continue
                    if arr[pointrow+row][pointcol+col] in has:
                        return False
                    has.add(arr[pointrow+row][pointcol+col])
        return True

def solve(bo):
    find = find_empty(bo)
    if not find:  # if find is None or False
        return True
    else:
        row, col = find

    for num in range(1, 10):
        if valid(bo, num, (row, col)):
            bo[row][col] = num

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):

    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0:
            if i == 0:
                print(" ┎─────────┰─────────┰─────────┒")
            else:
                print(" ┠─────────╂─────────╂─────────┨")

        for j in range(len(bo[0])):
            if j % 3 == 0:
                print(" ┃ ", end=" ")

            if j == 8:
                print(bo[i][j], " ┃")
            else:
                print(bo[i][j], end=" ")

    print(" ┖─────────┸─────────┸─────────┚")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # row, column

    return None

#print_board(board)
#solve(board)
#print_board(board)
