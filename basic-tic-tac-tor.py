def print_board(spots):
    print("\n" + "="*20)  # Visual separator
    print(f"{spots[1]}|{spots[2]}|{spots[3]}")
    print("-+-+-")
    print(f"{spots[4]}|{spots[5]}|{spots[6]}")
    print("-+-+-")
    print(f"{spots[7]}|{spots[8]}|{spots[9]}")
    print("="*20 + "\n")

def check_turn(turn):
    return 'X' if turn % 2 == 0 else 'O'

def check_for_win(spots):
    win_conditions = [
        [1,2,3],[4,5,6],[7,8,9],  # rows
        [1,4,7],[2,5,8],[3,6,9],  # columns
        [1,5,9],[3,5,7]           # diagonals
    ]
    for a,b,c in win_conditions:
        if spots[a] == spots[b] == spots[c] != ' ':
            return True
    return False

def main():
    print("=======================================")
    print(" BASIC TIC-TAC-TOE (2 PLAYERS)")
    print("=======================================")
    
    spots = {1:' ',2:' ',3:' ',
             4:' ',5:' ',6:' ',
             7:' ',8:' ',9:' '}
    
    turn = 0
    move_history = []  # Track all moves
    
    while True:
        print_board(spots)
        print(f"Moves so far: {move_history}" if move_history else "")
        
        current_player = check_turn(turn + 1)
        print(f"Player {current_player}'s turn (1-9) or 'q' to quit:")
        
        choice = input().strip().lower()
        
        if choice == 'q':
            print("\nGame aborted!")
            break
            
        if not choice.isdigit() or int(choice) not in spots:
            print("Invalid input! Use 1-9 or 'q'.")
            continue
            
        position = int(choice)
        if spots[position] != ' ':
            print("Spot taken! Try again.")
            continue
            
        # Record and make move
        move_history.append(f"{current_player}:{position}")
        turn += 1
        spots[position] = current_player
        
        # Check game state
        if check_for_win(spots):
            print_board(spots)
            print(f"Player {current_player} wins!")
            print(f"Winning moves: {move_history}")
            break
            
        if turn == 9:
            print_board(spots)
            print("It's a draw!")
            print(f"All moves: {move_history}")
            break

    print("Thanks for playing!")

if __name__ == "__main__":
    main()