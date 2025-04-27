from random import choice
from math import inf

# Initial state
S0 = {1: ' ', 2: ' ', 3: ' ',
      4: ' ', 5: ' ', 6: ' ',
      7: ' ', 8: ' ', 9: ' '}

def printBoard(board):
    print(board[1] + "|" + board[2] + "|" + board[3])
    print("-+-+-")
    print(board[4] + "|" + board[5] + "|" + board[6])
    print("-+-+-")
    print(board[7] + "|" + board[8] + "|" + board[9])
    print("\n")

def PLAYER(s):
    # Count number of X and O to determine whose turn it is
    x_count = sum(1 for v in s.values() if v == 'X')
    o_count = sum(1 for v in s.values() if v == 'O')
    return 'X' if x_count == o_count else 'O'

def ACTIONS(s):
    return [k for k, v in s.items() if v == ' ']

def RESULT(s, a):
    # Create a new copy of the state
    new_state = s.copy()
    new_state[a] = PLAYER(s)
    return new_state

def TERMINAL(s):
    # Check if someone won
    win_conditions = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
        [1, 5, 9], [7, 5, 3]              # diagonals
    ]
    for condition in win_conditions:
        if s[condition[0]] == s[condition[1]] == s[condition[2]] != ' ':
            return True
    
    # Check if board is full (draw)
    return all(v != ' ' for v in s.values())

def UTILITY(s):
    # Check if X won
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
    return 0  # draw

def MAX_VALUE(s, alpha, beta):
    if TERMINAL(s):
        return UTILITY(s)
    v = -inf
    for action in ACTIONS(s):
        v = max(v, MIN_VALUE(RESULT(s, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break  # Beta cutoff
    return v

def MIN_VALUE(s, alpha, beta):
    if TERMINAL(s):
        return UTILITY(s)
    v = inf
    for action in ACTIONS(s):
        v = min(v, MAX_VALUE(RESULT(s, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break  # Alpha cutoff
    return v

def playerMove(board):
    while True:
        try:
            position = int(input("Enter a position (1-9): "))
            if position < 1 or position > 9:
                print("Invalid position! Please choose between 1-9.")
            elif board[position] != ' ':
                print("Position already taken! Try another one.")
            else:
                return position
        except ValueError:
            print("Please enter a valid number!")

def compMove(board):
    best_score = -inf
    best_action = None
    alpha = -inf
    beta = inf
    
    for action in ACTIONS(board):
        new_state = RESULT(board, action)
        score = MIN_VALUE(new_state, alpha, beta)
        if score > best_score:
            best_score = score
            best_action = action
        alpha = max(alpha, best_score)
    return best_action

def main():
    board = S0.copy()
    print("=======================================")
    print("TIC-TAC-TOE with ALPHA-BETA PRUNING")
    print("=======================================")
    printBoard(board)
    
    # Randomly decide who goes first
    first_move = choice(['player', 'computer'])
    print(f"Randomly decided: {first_move.capitalize()} goes first!\n")
    
    current_player = 'O' if first_move == 'player' else 'X'
    
    while not TERMINAL(board):
        if current_player == 'O':  # Player's turn
            move = playerMove(board)
            board[move] = 'O'
            printBoard(board)
            current_player = 'X'
        else:  # Computer's turn
            print("Computer's turn (X):")
            move = compMove(board)
            board[move] = 'X'
            printBoard(board)
            current_player = 'O'

    # Game over, print result
    result = UTILITY(board)
    if result == 1:
        print("Computer (X) wins!")
    elif result == -1:
        print("Player (O) wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()