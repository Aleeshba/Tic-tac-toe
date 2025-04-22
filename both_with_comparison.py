import time
from random import choice
from math import inf

S0 = {i: ' ' for i in range(1, 10)}

def printBoard(board):
    print(board[1] + "|" + board[2] + "|" + board[3])
    print("-+-+-")
    print(board[4] + "|" + board[5] + "|" + board[6])
    print("-+-+-")
    print(board[7] + "|" + board[8] + "|" + board[9])
    print("\n")

def PLAYER(s):
    x_count = sum(1 for v in s.values() if v == 'X')
    o_count = sum(1 for v in s.values() if v == 'O')
    return 'X' if x_count == o_count else 'O'

def ACTIONS(s):
    return [k for k, v in s.items() if v == ' ']

def RESULT(s, a):
    new_state = s.copy()
    new_state[a] = PLAYER(s)
    return new_state

def TERMINAL(s):
    win_conditions = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [7, 5, 3]
    ]
    for condition in win_conditions:
        if s[condition[0]] == s[condition[1]] == s[condition[2]] != ' ':
            return True
    return all(v != ' ' for v in s.values())

def UTILITY(s):
    win_conditions = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [7, 5, 3]
    ]
    for condition in win_conditions:
        if s[condition[0]] == s[condition[1]] == s[condition[2]] == 'X':
            return 1
        if s[condition[0]] == s[condition[1]] == s[condition[2]] == 'O':
            return -1
    return 0

# Tracking variables for comparison
minimax_nodes = 0
alphabeta_nodes = 0

def MINIMAX_MAX(s):
    global minimax_nodes
    minimax_nodes += 1
    if TERMINAL(s):
        return UTILITY(s)
    v = -inf
    for a in ACTIONS(s):
        v = max(v, MINIMAX_MIN(RESULT(s, a)))
    return v

def MINIMAX_MIN(s):
    global minimax_nodes
    minimax_nodes += 1
    if TERMINAL(s):
        return UTILITY(s)
    v = inf
    for a in ACTIONS(s):
        v = min(v, MINIMAX_MAX(RESULT(s, a)))
    return v

def ALPHABETA_MAX(s, alpha, beta):
    global alphabeta_nodes
    alphabeta_nodes += 1
    if TERMINAL(s):
        return UTILITY(s)
    v = -inf
    for a in ACTIONS(s):
        v = max(v, ALPHABETA_MIN(RESULT(s, a), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def ALPHABETA_MIN(s, alpha, beta):
    global alphabeta_nodes
    alphabeta_nodes += 1
    if TERMINAL(s):
        return UTILITY(s)
    v = inf
    for a in ACTIONS(s):
        v = min(v, ALPHABETA_MAX(RESULT(s, a), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v

def compMoveCompare(board):
    global minimax_nodes, alphabeta_nodes

    minimax_nodes = 0
    alphabeta_nodes = 0

    start_min = time.time()
    best_score_min = -inf
    best_action_min = None
    for a in ACTIONS(board):
        score = MINIMAX_MIN(RESULT(board, a))
        if score > best_score_min:
            best_score_min = score
            best_action_min = a
    end_min = time.time()

    start_ab = time.time()
    best_score_ab = -inf
    best_action_ab = None
    for a in ACTIONS(board):
        score = ALPHABETA_MIN(RESULT(board, a), -inf, inf)
        if score > best_score_ab:
            best_score_ab = score
            best_action_ab = a
    end_ab = time.time()

    print("Minimax:     Move =", best_action_min, ", Time =", round(end_min - start_min, 5), "s, Nodes =", minimax_nodes)
    print("Alpha-Beta:  Move =", best_action_ab, ", Time =", round(end_ab - start_ab, 5), "s, Nodes =", alphabeta_nodes)
    return best_action_ab  # Actually play Alpha-Beta

def playerMove(board):
    while True:
        try:
            pos = int(input("Enter a position (1-9): "))
            if pos < 1 or pos > 9:
                print("Invalid position!")
            elif board[pos] != ' ':
                print("Already taken!")
            else:
                return pos
        except ValueError:
            print("Enter a number!")

def main():
    board = S0.copy()
    print("==============================")
    print("TIC-TAC-TOE: Minimax vs Alpha-Beta")
    print("==============================")
    printBoard(board)

    first = choice(['player', 'computer'])
    print(f"{first.capitalize()} goes first!\n")
    current = 'O' if first == 'player' else 'X'

    while not TERMINAL(board):
        if current == 'O':
            move = playerMove(board)
            board[move] = 'O'
        else:
            print("Computer's turn:")
            move = compMoveCompare(board)
            board[move] = 'X'
        printBoard(board)
        current = 'O' if current == 'X' else 'X'

    result = UTILITY(board)
    print("Game Over:")
    if result == 1:
        print("Computer (X) wins!")
    elif result == -1:
        print("Player (O) wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
