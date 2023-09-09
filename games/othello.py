import sys
from common.readme import updateReadme, format_time
from common.issue import GetInfo
from common.data import load_common_data, save_data

# Load data
def load_data():
    data, gameOver = load_common_data("games/othello_data/data.json")

    if "board" not in data or gameOver:
        data["board"] = [[-1] * 8 for i in range(8)]
        data["board"][3][3] = 0
        data["board"][3][4] = 1
        data["board"][4][3] = 1
        data["board"][4][4] = 0
        print("New board created")
    
    if "average_blue" not in data:
        data["average_blue"] = []

    if "average_green" not in data:
        data["average_green"] = []

    return data

def flip_piece(x, y, dirx, diry,first=True):
    board = data["board"]
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    if board[x][y] == data["turn"]:
        return not first
    if board[x][y] == -1:
        return False
    if flip_piece(x + dirx, y + diry, dirx, diry,False):
        board[x][y] = data["turn"]
        return True
    return False

def flip_piece_test(x, y, dirx,diry,turn,first=True):
    board = data["board"]
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    if board[x][y] == turn:
        return not first
    if board[x][y] == -1:
        return False
    if flip_piece_test(x + dirx, y + diry, dirx, diry,turn,False):
        return True
    return False

def make_move():
    board = data["board"]

    # Check if move is valid
    if board[move[0]][move[1]] != -1:
        return False, "That space is already taken"
    
    # Make move
    board[move[0]][move[1]] = data["turn"]
    valid = False
    valid = flip_piece(move[0] - 1, move[1], -1, 0) or valid
    valid = flip_piece(move[0] + 1, move[1], 1, 0) or valid
    valid = flip_piece(move[0], move[1] - 1, 0, -1) or valid
    valid = flip_piece(move[0], move[1] + 1, 0, 1) or valid
    valid = flip_piece(move[0] - 1, move[1] - 1, -1, -1) or valid
    valid = flip_piece(move[0] + 1, move[1] - 1, 1, -1) or valid
    valid = flip_piece(move[0] - 1, move[1] + 1, -1, 1) or valid
    valid = flip_piece(move[0] + 1, move[1] + 1, 1, 1) or valid

    if not valid:
        return False, "That move is invalid"

    # Check for win
    for i in range(8):
        for j in range(8):
            if board[i][j] == -1:
                return True, "continue"

    return True, "win"

# Get move
def get_move():
    if issue.title.lower().startswith("othello:"):
        input = issue.title.split(":")[1].split(' ')[-1]
        return [int(input[1]), ord(input[0].upper()) - 65]
    return [-1, -1]

# Generate Valid Moves for Othello
def generate_moves(nextTurn):
    moves = []
    for i in range(8):
        for j in range(8):
            if data["board"][i][j] != -1: continue
            valid = False
            valid = flip_piece_test(i - 1, j, -1, 0,nextTurn) or valid
            valid = flip_piece_test(i + 1, j, 1, 0,nextTurn) or valid
            valid = flip_piece_test(i, j - 1, 0, -1,nextTurn) or valid
            valid = flip_piece_test(i, j + 1, 0, 1,nextTurn) or valid
            valid = flip_piece_test(i - 1, j - 1, -1, -1,nextTurn) or valid
            valid = flip_piece_test(i + 1, j - 1, 1, -1,nextTurn) or valid
            valid = flip_piece_test(i - 1, j + 1, -1, 1,nextTurn) or valid
            valid = flip_piece_test(i + 1, j + 1, 1, 1,nextTurn) or valid
            if valid:
                moves.append([i,j])
    return moves

def generate_moves_newGame(nextTurn):
    if nextTurn == 0:
        return [[3,2],[2,3],[5,4],[4,5]]
    else:
        return [[2,2],[3,3],[4,4],[5,5]]

# Update data
def update_data(move, state):
    currentWinner = ""
    previousColor = "Blue" if data["turn"] == 0 else "Green"
    previousDot = "🔵" if data["turn"] == 0 else "🟢"
    data["history"] = [[f"{'🔵' if data['turn'] == 0 else '🟢'} {chr(65+move[1])}{move[0]}", user]] + data["history"]

    # Get count
    piece_count = [0, 0]
    for i in range(8):
        for j in range(8):
            if data["board"][i][j] != -1:
                piece_count[data["board"][i][j]] += 1

    # Save data
    nextTurn = 1 - data["turn"]

    if state == "win":
        data["average_blue"].append(piece_count[0])
        data["average_green"].append(piece_count[1])
        if piece_count[0] == piece_count[1]:
            state = "draw"
            currentWinner = "🔵 It is a draw. 🟢"
        else:
            currentWinner = f"{previousDot} {previousColor} wins! {previousDot}"
        moves = generate_moves_newGame(nextTurn)
    else:
        # Generate moves
        moves = generate_moves(nextTurn)
        if len(moves) == 0:
            data["turn"] = 1 - data["turn"]
            nextTurn = 1 - data["turn"]
            moves = generate_moves(nextTurn)
            if len(moves) == 0:
                state = "draw"
                currentWinner = "🔵 It is a draw. 🟢"
                moves = generate_moves_newGame(nextTurn)

    
    save_data(data, state, user, "games/othello_data/data.json")

    # Update readme
    color = "Blue" if nextTurn == 0 else "Green"
    dot = "🔵" if nextTurn == 0 else "🟢"

    # Create Board
    imgs = ['common/blank.png', 'othello_data/blue.svg', 'othello_data/green.svg']
    value = '|  | A | B | C | D | E | F | G | H |\n| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |\n'
    
    movesAsStrings = [f'{i}-{j}' for i,j in moves]
    
    for i in range(8):
        value += f'| {i} |'
        for j in range(8):
            if f'{i}-{j}' in movesAsStrings:
                value += f" <a href='https://github.com/BenjaminHalko/BenjaminHalko/issues/new?title=Othello:+{chr(65+j)}{i}&body=Please+do+not+change+the+title.+Just+click+\"Submit+new+issue\".+You+do+not+need+to+do+anything+else.+%3AD'><img src='https://github.com/BenjaminHalko/BenjaminHalko/raw/main/games/othello_data/marker.svg' alt='marker' width='50px'></a> |"
            else:
                value += f' <img src="https://github.com/BenjaminHalko/BenjaminHalko/raw/main/games/{imgs[data["board"][i][j]+1]}" alt="{imgs[data["board"][i][j]+1].split("/")[1].split(".")[0]}" width="50px"> |'
        value += '\n'

    # Update stats
    stats = {
        "Blue Wins": data["games_won"][0],
        "Green Wins": data["games_won"][1]
    }

    if data["games_won"][2] > 0:
        stats["Draws"] = data["games_won"][2]

    if len(data["game_times"]) > 0:
        stats["Average Blue Pieces"] = sum(data["average_blue"]) / len(data["average_blue"])
        stats["Average Green Pieces"] = sum(data["average_green"]) / len(data["average_green"])
        stats["Average Time per Game"] = format_time(sum(data["game_times"]) / len(data["game_times"]))

    readmeMoves = ""
    info = f"<b>A game of Othello played on GitHub.</b><br>Click on a white dot to make your move.<br>Blue has {piece_count[0]} pieces. Green has {piece_count[1]} pieces.<br>{dot} It is currently {color}'s turn. {dot}"
    if "game_over" in data:
        info = f"<b>A game of Othello played on GitHub.</b><br>The game is currently over. {currentWinner}<br>Use the chart below to start a new game."
        readmeMoves = '\n<details align="left"><summary><h3>Available Moves</h3></summary>\n<p align="left">\n'
        for i,move in enumerate(moves):
            if i != 0: readmeMoves += ", "
            readmeMoves += f"<a href='https://github.com/BenjaminHalko/BenjaminHalko/issues/new?title=Othello:+{chr(65+move[1])}{move[0]}&body=Please+do+not+change+the+title.+Just+click+\"Submit+new+issue\".+You+do+not+need+to+do+anything+else.+%3AD'>{chr(65+move[1])}{move[0]}</a>"
        readmeMoves += "</p>\n"
        readmeMoves += "</details>\n"

    updateReadme("Othello","OTHELLO",info,value,data["leaderboard"],data["history"],stats,readmeMoves)

# Main
if __name__ == "__main__":
    issue, user = GetInfo()
    try:
        data = load_data()
        turn = data["turn"]

        move = get_move()
        success, state = make_move()
        print(state)
        if not success:
            issue.create_comment("Sorry, that move is invalid. Please try again.")
            issue.edit(state="closed", labels=['Invalid'])
            sys.exit(1)

        update_data(move, state)
        
        # Create comment
        issue.create_comment(f"@{user} Thanks for playing Othello! See the readme for the updated board.")
        issue.edit(state="closed", labels=['Blue' if turn == 0 else 'Green'])
    except Exception as e:
        print(e)
        issue.create_comment("Sorry, something went wrong. Please try again.")
        issue.edit(state="closed", labels=['Invalid'])
        sys.exit(1)


