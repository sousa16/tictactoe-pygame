def available_square(board, row, col):  # checks if a square is empty
    return board[row][col] == 0


def mark_square(board, row, col, p):  # marks a square with p (0 or 1) and returns the board after marking
    board[row][col] = p
    return board


def get_row(board, r):  # gets r row
    row = (board[r][0], board[r][1], board[r][2])
    return row


def get_col(board, c):  # gets c column
    col = (board[0][c], board[1][c], board[2][c])
    return col


def get_diag(board, d):  # gets d diagonal
    if d == 0:
        diagonal = (board[0][0], board[1][1], board[2][2])
    else:
        diagonal = (board[2][0], board[1][1], board[0][2])
    return diagonal


def win(board, p):  # returns a position if it is possible to win, 0 if not
    for a in range(0, 3):

        if get_row(board, a).count(p) == 2:
            for b in range(0, 3):
                if available_square(board, a, b):
                    return [a, b]
        elif get_col(board, a).count(p) == 2:
            for b in range(0, 3):
                if available_square(board, b, a):
                    return [b, a]

        elif a != 2 and get_diag(board, a).count(p) == 2:
            for b in range(0, 3):
                if a == 0:
                    if available_square(board, b, b):
                        return [b, b]
            if a == 1:
                for b in [[0, 2], [1, 1], [2, 0]]:
                    if available_square(board, b[0], b[1]):
                        return b

    return 0


def block(board, p):  # returns a position if it is possible to block opponent's win, 0 if not
    for a in range(0, 3):

        if get_row(board, a).count(-p) == 2:
            for b in range(0, 3):
                if available_square(board, a, b):
                    return [a, b]
        elif get_col(board, a).count(-p) == 2:
            for b in range(0, 3):
                if available_square(board, b, a):
                    return [b, a]

        elif a != 2 and get_diag(board, a).count(-p) == 2:
            for b in range(0, 3):
                if a == 0:
                    if available_square(board, b, b):
                        return [b, b]
            if a == 1:
                for b in [[0, 2], [1, 1], [2, 0]]:
                    if available_square(board, b[0], b[1]):
                        return b

    return 0


def bifurcation(board, p):  # returns a position if it is possible to create a bifurcation, 0 if not
    lin = []
    col = []
    dia = []
    bifpos = []

    for a in range(0, 3):

        if get_row(board, a).count(p) == 1 and get_row(board, a).count(-p) == 0:
            for b in range(0, 3):
                if available_square(board, a, b):
                    lin.append([a, b])

        if get_col(board, a).count(p) == 1 and get_col(board, a).count(-p) == 0:
            for b in range(0, 3):
                if available_square(board, b, a):
                    col.append([b, a])

        if a == 0 and get_diag(board, a).count(p) == 1 and get_diag(board, a).count(-p) == 0:
            for b in [[0, 0], [1, 1], [2, 2]]:
                if available_square(board, b[0], b[1]):
                    dia.append(b)
        elif a == 1 and get_diag(board, a).count(p) == 1 and get_diag(board, a).count(-p) == 0:
            for b in [[0, 2], [1, 1], [2, 0]]:
                if available_square(board, b[0], b[1]):
                    dia.append(b)

    for p in lin:
        if p in col:
            bifpos.append(p)
        if p in dia:
            bifpos.append(p)

    for p in col:
        if p in dia:
            bifpos.append(p)

    bifpos.sort()
    if len(bifpos) >= 1:
        return bifpos[0]

    return 0


def block_bifurcation(board, p):  # returns a position if it is possible to block an opponent's bifurcation, 0 if not
    lin = []
    col = []
    dia = []
    bifpos = []

    for a in range(0, 3):

        if get_row(board, a).count(-p) == 1 and get_row(board, a).count(p) == 0:
            for b in range(0, 3):
                if available_square(board, a, b):
                    lin.append([a, b])

        if get_col(board, a).count(-p) == 1 and get_col(board, a).count(p) == 0:
            for b in range(0, 3):
                if available_square(board, b, a):
                    col.append([b, a])

        if a == 0 and get_diag(board, a).count(-p) == 1 and get_diag(board, a).count(p) == 0:
            for b in [[0, 0], [1, 1], [2, 2]]:
                if available_square(board, b[0], b[1]):
                    dia.append(b)
        elif a == 1 and get_diag(board, a).count(-p) == 1 and get_diag(board, a).count(p) == 0:
            for b in [[0, 2], [1, 1], [2, 0]]:
                if available_square(board, b[0], b[1]):
                    dia.append(b)

    for pos in lin:
        if pos in col:
            bifpos.append(pos)
        if pos in dia:
            bifpos.append(pos)

    for pos in col:
        if pos in dia:
            bifpos.append(pos)

    bifpos.sort()

    if len(bifpos) == 1:
        return bifpos[0]

    elif len(bifpos) > 1:
        for pos in [[1, 0], [0, 1], [2, 1], [1, 2]]:
            if available_square(board, pos[0], pos[1]):
                return pos
    return 0


def center(board):  # returns center position if center is empty, 0 if not
    if available_square(board, 1, 1):
        return [1, 1]

    return 0


def opp_corner(board, p):  # returns a position if an opposite corner from CPU's piece is empty, 0 if not
    if board[0][0] == -p and available_square(board, 2, 2):
        return [2, 2]
    elif board[2][0] == -p and available_square(board, 0, 2):
        return [0, 2]
    elif board[0][2] == -p and available_square(board, 2, 0):
        return [2, 0]
    elif board[2][2] == -p and available_square(board, 0, 0):
        return [0, 0]

    return 0


def empty_corner(board):  # returns an empty corner if a corner is empty, 0 if not
    for a in [[0, 0], [2, 0], [0, 2], [2, 2]]:
        if available_square(board, a[0], a[1]):
            return a

    return 0


def empty_lateral(board):  # returns an empty lateral if a lateral is empty, 0 if not
    for a in [[1, 0], [0, 1], [2, 1], [1, 2]]:
        if available_square(board, a[0], a[1]):
            return a

    return 0


def auto_pick_pos(board, p, strat):  # combines all functions to apply the algorithms described on the README file
    if strat == 'EASY':

        if center(board) != 0:
            return center(board)
        elif empty_corner(board) != 0:
            return empty_corner(board)
        elif empty_lateral(board) != 0:
            return empty_lateral(board)

    elif strat == 'NORMAL':

        if win(board, p) != 0:
            return win(board, p)
        elif block(board, p) != 0:
            return block(board, p)
        elif center(board) != 0:
            return center(board)
        elif opp_corner(board, p) != 0:
            return opp_corner(board, p)
        elif empty_corner(board) != 0:
            return empty_corner(board)
        elif empty_lateral(board) != 0:
            return empty_lateral(board)

    else:

        if win(board, p) != 0:
            return win(board, p)
        elif block(board, p) != 0:
            return block(board, p)
        elif bifurcation(board, p) != 0:
            return bifurcation(board, p)
        elif block_bifurcation(board, p) != 0:
            return block_bifurcation(board, p)
        elif center(board) != 0:
            return center(board)
        elif opp_corner(board, p) != 0:
            return opp_corner(board, p)
        elif empty_corner(board) != 0:
            return empty_corner(board)
        elif empty_lateral(board) != 0:
            return empty_lateral(board)