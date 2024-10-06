import random
import time
def draw_board(board):
    columns = "\n    1   2   3   4   5"
    row_separator = "  ---------------------"
    
    print(columns)
    for i in range(5):
        row = f"{i + 1} | {' | '.join(board[i])} |"
        print(row)
        if i < 4:
            print(row_separator)

# Create a 5x5 board initialized with empty values
board = [[' ' for _ in range(5)] for _ in range(5)]

# Define the valid positions
valid_positions = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                   (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
                   (2, 1), (3, 1), (4, 1), (2, 5), (3, 5), (4, 5)]

def check_winner(board, current_symbol):
    # Check rows
    for row in board:
        if all(cell == current_symbol for cell in row):
            return True

    # Check cols
    for col in range(5):
        if all(board[row][col] == current_symbol for row in range(5)):
            return True

    # Check main diagonal
    if all(board[i][i] == current_symbol for i in range(5)):
        return True

    # Check secondary diagonal
    if all(board[i][4 - i] == current_symbol for i in range(5)):
        return True

    return False

def getIAfValues(options):
    try:
        print("\nAI entering values", end="")
        for i in range(4):  # Repeat 3 times to show from 1 to 3 dots
            print(".", end="", flush=True)  # Print a dot and keep the cursor on the same line
            time.sleep(0.50)  # Wait for 1 second
        print()  # Print a new line after the loop completes
        # Seleccionar aleatoriamente
        selection = random.choice(options)
        return selection
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return None

print("\n--WELCOME TO QUIXO!--")
while True:
    print("\nChoose your symbol:")
    print("1. X")
    print("2. O")
    choice = input("\nEnter your choice (1/2): ")
    
    if choice == '1':
        player_symbol = 'X'
        ai_symbol = 'O'
        break
    elif choice == '2':
        player_symbol = 'O'
        ai_symbol = 'X'
        break
    else:
        print("\nChoose a valid option")

current_symbol = player_symbol

while True:
    draw_board(board)

    while True:
        if current_symbol== ai_symbol:
            print("\nAI Turn")
            print("\nAI entering values", end="")
            for i in range(4):  # Repeat 3 times to show 1 to 3 points.
                print(".", end="", flush=True)  # Prints a dot and keeps the cursor on the same line
                time.sleep(0.50)  # Wait 1 second
            print()    # Prints a new line after the cycle completes
            while True:
                irow, icol = random.choice(valid_positions)
                if board[irow-1][icol-1] != player_symbol or board[irow-1][icol-1] != ' ':
                    break
        elif current_symbol == player_symbol:     
            print("\nPlayer turn")   
            # Ask the user for the initial row and column
            while True:
                try:
                    irow, icol = map(int, input(f"\nPlayer {current_symbol}, enter the row and column (1-5) that you want to choose (e.g., '1 2'): ").split())
                    if 1 <= irow <= 5 and 1 <= icol <= 5:
                        if (irow, icol) in valid_positions and (board[irow - 1][icol - 1] == ' ' or board[irow - 1][icol - 1] == current_symbol):
                            break
                        else:
                            print(f"The selected position does not contain your token ('{current_symbol}'). Please try again.")
                    else:
                        print("\nPlease enter two valid numbers between 1 and 5, separated by a space.")
                except ValueError:
                    print("Please enter two valid numbers between 1 and 5, separated by a space.")
        
        # Validate the initial position and verify if the card belongs to the current player.
        if (irow, icol) in valid_positions and (board[irow - 1][icol - 1] == ' ' or board[irow - 1][icol - 1] == current_symbol):
            while True:
                if(irow == 1 and icol == 1):
                    board[0][0] = current_symbol
                    draw_board(board)
                    board[0][0] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["down", "right"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to:  right or down (right/down) (c back to pick up card): ").lower()
                        
                        if answer == "right":
                            # Move to right
                            board[0][0] = board[0][1]
                            board[0][1] = board[0][2]
                            board[0][2] = board[0][3]
                            board[0][3] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[0][0] = board[1][0]
                            board[1][0] = board[2][0]
                            board[2][0] = board[3][0]
                            board[3][0] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'right' or 'down'")
                    break      
                elif(irow == 5 and icol == 5):
                    board[4][4] = current_symbol
                    draw_board(board)
                    board[4][4] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "up"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left or up (left/up) (c back to pick up card): ").lower()
                        
                        if answer == "left":
                            # Move to left
                            board[4][4] = board[4][3]
                            board[4][3] = board[4][2]
                            board[4][2] = board[4][1]
                            board[4][1] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "up":
                            # Move to up
                            board[4][4] = board[3][4]
                            board[3][4] = board[2][4]
                            board[2][4] = board[1][4]
                            board[1][4] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'left' or 'up'")
                elif(irow == 5 and icol == 1):
                    board[4][0] = current_symbol
                    draw_board(board)
                    board[4][0] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["right", "up"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: right or up (right/up) (c back to pick up card): ").lower()
                        if answer == "right":
                            # Move to right
                            board[4][0] = board[4][1]
                            board[4][1] = board[4][2]
                            board[4][2] = board[4][3]
                            board[4][3] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "up":
                            # Move to up
                            board[4][0] = board[4][0]
                            board[3][0] = board[3][0]
                            board[2][0] = board[2][0]
                            board[1][0] = board[1][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'right' or 'up'")
                elif(irow == 1 and icol == 5):
                    board[0][4] = current_symbol
                    draw_board(board)
                    board[0][4] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "down"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left or down (left/down) (c back to pick up card): ").lower()
                        if answer == "left":
                            # Move to left
                            board[0][4] = board[0][3]
                            board[0][3] = board[0][2]
                            board[0][2] = board[0][1]
                            board[0][1] = board[0][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[0][4] = board[1][4]
                            board[1][4] = board[2][4]
                            board[2][4] = board[3][4]
                            board[3][4] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'up', 'down' or 'right'")
                elif(irow == 1 and icol == 2):
                    board[0][1] = current_symbol
                    draw_board(board)
                    board[0][1] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "right", "down"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left, right or down (left/right/down) (c back to pick up card): ").lower()
                        
                        if answer == "left":
                            # Move to left
                            board[0][1] = board[0][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[0][1] = board[0][2]
                            board[0][2] = board[0][3]
                            board[0][3] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[0][1] = board[1][1]
                            board[1][1] = board[2][1]
                            board[2][1] = board[3][1]
                            board[3][1] = board[4][1]
                            board[4][1] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'left' or 'down'")
                elif(irow == 1 and icol == 3):
                    board[0][2] = current_symbol
                    draw_board(board)
                    board[0][2] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "right", "down"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left, right or down (left/right/down) (c back to pick up card): ").lower()
                        
                        if answer == "left":
                            # Move to left
                            board[0][2] = board[0][1]
                            board[0][1] = board[0][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[0][2] = board[0][3]
                            board[0][3] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[0][2] = board[1][2]
                            board[1][2] = board[2][2]
                            board[2][2] = board[3][2]
                            board[3][2] = board[4][2]
                            board[4][2] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'left' or 'down'")    
                elif(irow == 1 and icol == 4):
                    board[0][3] = current_symbol
                    draw_board(board)
                    board[0][3] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "right", "down"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left, right or down (left/right/down) (c back to pick up card): ").lower()
                        
                        if answer == "left":
                            # Move to left
                            board[0][3] = board[0][2]
                            board[0][2] = board[0][1]
                            board[0][3] = board[0][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[0][3] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[0][3] = board[1][3]
                            board[1][3] = board[2][3]
                            board[2][3] = board[3][3]
                            board[3][3] = board[4][3]
                            board[4][3] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'left' or 'down'")    
                elif(irow == 2 and icol == 1):
                    board[1][0] = current_symbol
                    draw_board(board)
                    board[1][0] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["up", "down", "right"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: up, down or right (up/down/right) (c back to pick up card): ").lower()
                        
                        if answer == "up":
                            # Move to up
                            board[1][0] = board[0][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[1][0] = board[2][0]
                            board[2][0] = board[3][0]
                            board[3][0] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[1][0] = board[1][1]
                            board[1][1] = board[1][2]
                            board[1][2] = board[1][3]
                            board[1][3] = board[1][4]
                            board[1][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'up', 'down' or 'right'")    
                elif(irow == 3 and icol == 1):
                    board[2][0] = current_symbol
                    draw_board(board)
                    board[2][0] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["up", "down", "right"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: up, down or right (up/down/right) (c back to pick up card): ").lower()

                        if answer == "up":
                            # Move to up
                            board[2][0] = board[1][0]
                            board[1][0] = board[0][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[2][0] = board[3][0]
                            board[3][0] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[2][0] = board[2][1]
                            board[2][1] = board[2][2]
                            board[2][2] = board[2][3]
                            board[2][3] = board[2][4]
                            board[2][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'up', 'down' or 'right'")    
                elif(irow == 4 and icol == 1):
                    board[3][0] = current_symbol
                    draw_board(board)
                    board[3][0] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["up", "down", "right"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: up, down or right (up/down/right) (c back to pick up card): ").lower()
                        
                        if answer == "up":
                            # Move to up
                            board[3][0] = board[2][0]
                            board[2][0] = board[1][0]
                            board[1][0] = board[0][0]
                            board[0][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[3][0] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[3][0] = board[3][1]
                            board[3][1] = board[3][2]
                            board[3][2] = board[3][3]
                            board[3][3] = board[3][4]
                            board[3][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'up', 'down' or 'right'")    
                elif(irow == 5 and icol == 2):
                    board[4][1] = current_symbol
                    draw_board(board)
                    board[4][1] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "right", "up"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left, right or up (left/right/up) (c back to pick up card): ").lower()
                    
                        if answer == "left":
                            # Move to left
                            board[4][1] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[4][1] = board[4][2]
                            board[4][2] = board[4][3]
                            board[4][3] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "up":
                            # Move to up
                            board[4][1] = board[3][1]
                            board[3][1] = board[2][1]
                            board[2][1] = board[1][1]
                            board[1][1] = board[0][1]
                            board[0][1] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'left', 'right' or 'up'") 
                elif(irow == 5 and icol == 3):
                    board[4][2] = current_symbol
                    draw_board(board)
                    board[4][2] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "right", "up"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left, right or up (left/right/up) (c back to pick up card): ").lower()

                        if answer == "left":
                            # Move to left
                            board[4][2] = board[4][1]
                            board[4][1] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[4][2] = board[4][3]
                            board[4][3] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "up":
                            # Move to up
                            board[4][2] = board[3][2]
                            board[3][2] = board[2][2]
                            board[2][2] = board[1][2]
                            board[1][2] = board[0][2]
                            board[0][2] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'left', 'right' or 'up'")
                
                elif(irow == 5 and icol == 4):
                    board[4][3] = current_symbol
                    draw_board(board)
                    board[4][3] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["left", "right", "up"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: left, right or up (left/right/up) (c back to pick up card): ").lower()

                        if answer == "left":
                            # Move to left
                            board[4][3] = board[4][2]
                            board[4][2] = board[4][1]
                            board[4][1] = board[4][0]
                            board[4][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "right":
                            # Move to right
                            board[4][3] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "up":
                            # Move to up
                            board[4][3] = board[3][3]
                            board[3][3] = board[2][3]
                            board[2][3] = board[1][3]
                            board[1][3] = board[0][3]
                            board[0][3] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'left', 'right' or 'up'")
                
                elif(irow == 2 and icol == 5):
                    board[1][4] = current_symbol
                    draw_board(board)
                    board[1][4] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["up", "down", "left"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: up, down or left (up/down/left) (c back to pick up card): ").lower()
                        
                        if answer == "up":
                            # Move to up
                            board[1][4] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[1][4] = board[2][4]
                            board[2][4] = board[3][4]
                            board[3][4] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "left":
                            # Move to left
                            board[1][4] = board[1][3]
                            board[1][3] = board[1][2]
                            board[1][2] = board[1][1]
                            board[1][1] = board[1][0]
                            board[1][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'up', 'down' or 'left'")
                elif(irow == 3 and icol == 5):
                    board[2][4] = current_symbol
                    draw_board(board)
                    board[2][4] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["up", "down", "left"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to:  up, down or left (up/down/left) (c back to pick up card): ").lower()

                        if answer == "up":
                            # Move to up
                            board[2][4] = board[1][4]
                            board[1][4] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[2][4] = board[3][4]
                            board[3][4] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "left":
                            # Move to left
                            board[2][4] = board[2][3]
                            board[2][3] = board[2][2]
                            board[2][2] = board[2][1]
                            board[2][1] = board[2][0]
                            board[2][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'up', 'down' or 'left'")
                
                elif(irow == 4 and icol == 5):
                    board[3][4] = current_symbol
                    draw_board(board)
                    board[3][4] = ' '
                    while(True):
                        if current_symbol == ai_symbol:
                            options = ["up", "down", "left"]
                            answer = getIAfValues(options)
                        elif current_symbol == player_symbol:
                            answer = input("\nChoose where to move it to: up, down or left (up/down/left) (c back to pick up card): ").lower()
                        
                        if answer == "up":
                            # Move to up
                            board[3][4] = board[1][4]
                            board[2][4] = board[1][4]
                            board[1][4] = board[0][4]
                            board[0][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "down":
                            # Move to down
                            board[3][4] = board[4][4]
                            board[4][4] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "left":
                            # Move to left
                            board[3][4] = board[3][3]
                            board[3][3] = board[3][2]
                            board[3][2] = board[3][1]
                            board[3][1] = board[3][0]
                            board[3][0] = current_symbol
                            draw_board(board)
                            break
                        elif answer == "c":
                            break
                        else:
                            print("Enter a valid answer 'up', 'down' or 'left'.")
                break  
        else:
            print(f"The selected position does not contain your token ('{current_symbol}'). Please try again.")
        
         # Check if there is a winner after placing the current_symbol
        if check_winner(board, current_symbol):
            draw_board(board)
            print(f"\nCongratulations, the player {current_symbol} has won!\n")
            break  # Exiting the loop if there is a winner

        if answer != "c":
            # Alternate the current_symbol after each turn
            current_symbol = ai_symbol if current_symbol== player_symbol else player_symbol
    break