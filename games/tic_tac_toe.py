import re
import urllib.parse
import json

def update_board(board, move, player):
    if board[move] == 'X' or board[move] == 'O':
        return False
    board[move] = player
    return True

def check_winner(board):
    # Define the winning combinations
    winning_combinations = [
        [0, 1, 2], # Top row
        [3, 4, 5], # Middle row
        [6, 7, 8], # Bottom row
        [0, 3, 6], # Left column
        [1, 4, 7], # Middle column
        [2, 5, 8], # Right column
        [0, 4, 8], # Diagonal from top-left to bottom-right
        [2, 4, 6]  # Diagonal from top-right to bottom-left
    ]

    # Check each winning combination
    for combination in winning_combinations:
        a, b, c = combination
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]

    # Check for a draw (if all positions are filled and no winner)
    if all(cell != "" for cell in board):
        return "Draw"

    # No winner and not a draw
    return None

def update_readme(board, status):
    with open('README.md', 'r') as file:
        content = file.read()

    updated_board = ['&nbsp;' if tile == ' ' else tile for tile in board]

    board_str = f"""| {updated_board[0]} | {updated_board[1]} | {updated_board[2]} |
|---|---|---|
| {updated_board[3]} | {updated_board[4]} | {updated_board[5]} |
| {updated_board[6]} | {updated_board[7]} | {updated_board[8]} |"""

    with open('games/ttt_data/data.json', 'r') as file:
        data = json.load(file)
    data['board'] = updated_board  # Update board in data dictionary

    possible_moves = [i+1 for i, v in enumerate(board) if v == ' ']
    moves_str = "Possible moves:\n\n"
    i = 0
    for move in possible_moves:
        if updated_board[i] == 'X' or updated_board[i] == 'O':
            pass
        else:
            issue_title = f"move {move}"
            encoded_title = urllib.parse.quote(issue_title)
            moves_str += f"- [Move {move}](https://github.com/Coding4Hours/Coding4Hours/issues/new?title={encoded_title})\n"
        i += 1

    new_content = re.sub(r'## Current Board\n\n.*?\n\n', f'## Current Board\n\n{board_str}\n\n', content, flags=re.DOTALL)
    new_content = re.sub(r'## Game Status\n\n.*', f'## Game Status\n\n{status}', new_content)

    with open('README.md', 'w') as file:
        file.write(new_content)

    # If you need to persist the updated board in "ttt_data/data.json"
    with open('games/ttt_data/data.json', 'w') as file:
        json.dump(data, file)
    

import sys
if len(sys.argv) > 1:
    move = int(sys.argv[1]) - 1
    with open('README.md', 'r') as file:
        content = file.read()
    
    with open('games/ttt_data/data.json', 'r') as file:
        data = json.load(file) 
    board = data['board']
    
    current_player = data['turn']

    print(board)
    
    if update_board(board, move, current_player):
        winner = check_winner(board)
        if winner:
            status = f'{winner} wins!' if winner != 'Tie' else "It's a tie!"
            board_str = f"""|  |  |  |
            |---|---|---|
            |  |  |  |
            |  |  |  |"""
            with open('games/ttt_data/data.json', 'r') as file:
                data = json.load(file)
            data['board'] = updated_board  # Update board in data dictionary

            possible_moves = [i+1 for i, v in enumerate(board) if v == ' ']
            moves_str = "Possible moves:\n\n"
            i = 0
            for move in possible_moves:
                if updated_board[i] == 'X' or updated_board[i] == 'O':
                    pass
                else:
                    issue_title = f"move {move}"
                    encoded_title = urllib.parse.quote(issue_title)
                    moves_str += f"- [Move {move}](https://github.com/Coding4Hours/Coding4Hours/issues/new?title={encoded_title})\n"
                i += 1

            new_content = re.sub(r'## Current Board\n\n.*?\n\n', f'## Current Board\n\n{board_str}\n\n', content, flags=re.DOTALL)
            new_content = re.sub(r'## Game Status\n\n.*', f'## Game Status\n\n{status}', new_content)

            with open('README.md', 'w') as file:
                file.write(new_content)




        
        else:
            next_player = 'O' if current_player == 'X' else 'X'
            status = f"It's {next_player}'s turn to play."
        
        with open('games/ttt_data/data.json', 'r') as file:
            a = json.load(file)
            
        a['turn'] = 'O' if current_player == 'X' else 'X'
        with open('games/ttt_data/data.json', 'w') as file:
            file.write(json.dumps(a))
        update_readme(board, status)
