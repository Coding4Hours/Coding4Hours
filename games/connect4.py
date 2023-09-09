import sys
from common.readme import updateReadme, format_time
from common.issue import GetInfo
from common.data import load_common_data, save_data

# Load data
def load_data():
    data, gameOver = load_common_data("games/connect4_data/data.json")

    if "board" not in data or gameOver:
        data["board"] = [[-1] * 6 for i in range(8)]
        print("New board created")

    return data

# Make a move
def make_move():
    board = data["board"]

    # Check if move is valid
    if board[move][0] != -1:
        return False, "That column is full"
    
    # Make move
    for i in range(5,-1,-1):
        if board[move][i] == -1:
            data["board"][move][i] = data["turn"]
            break
    
    # Check for win
    # Check horizontal
    for i in range(5):
        for j in range(6):
            if board[i][j] == data["turn"] and board[i + 1][j] == data["turn"] and board[i + 2][j] == data["turn"] and board[i + 3][j] == data["turn"]:
                return True, "win"
        
    # Check vertical
    for i in range(8):
        for j in range(3):
            if board[i][j] == data["turn"] and board[i][j + 1] == data["turn"] and board[i][j + 2] == data["turn"] and board[i][j + 3] == data["turn"]:
                return True, "win"
            
    # Check diagonal
    for i in range(5):
        for j in range(3):
            if board[i][j] == data["turn"] and board[i + 1][j + 1] == data["turn"] and board[i + 2][j + 2] == data["turn"] and board[i + 3][j + 3] == data["turn"]:
                return True, "win"
            
    for i in range(5):
        for j in range(3):
            if board[i][j + 3] == data["turn"] and board[i + 1][j + 2] == data["turn"] and board[i + 2][j + 1] == data["turn"] and board[i + 3][j] == data["turn"]:
                return True, "win"
            
    # Check for draw
    for i in range(8):
        if board[i][0] == -1:
            return True, "continue"
        
    return True, "draw"

# Get move
def get_move():
    if issue.title.lower().startswith("connect4:"):
        return int(issue.title.split(":")[1].split(' ')[-1])
    return -1

# Main
if __name__ == "__main__":
    issue, user = GetInfo()
    try:
        data = load_data()
        move = get_move()
        success, state = make_move()
        print(state)
        if not success:
            issue.create_comment("Sorry, that move is invalid. Please try again.")
            issue.edit(state="closed", labels=['Invalid'])
            sys.exit(1)

        currentWinner = ""
        previousColor = "Red" if data["turn"] == 0 else "Yellow"
        previousDot = '🔴' if data["turn"] == 0 else '🟡'
        data["history"] = [[f"{'🔴' if data['turn'] == 0 else '🟡'} Column {move}", user]] + data["history"]

        if state == "win":
            currentWinner = f"{previousDot} {previousColor} wins! {previousDot}"
        elif state == "draw":
            currentWinner = "🔴 It is a draw. 🟡"
        
        # Save data
        nextTurn = 1 - data["turn"]
        save_data(data, state, user, "games/connect4_data/data.json")

        # Update readme
        color = "Red" if nextTurn == 0 else "Yellow"
        dot = '🔴' if nextTurn == 0 else '🟡' 

        # Create Board
        imgs = ['common/blank.png', 'connect4_data/red.svg', 'connect4_data/yellow.svg']
        value = ''
        for i in range(8):
            link = f'COL {i}'
            if data["board"][i][0] == -1:
                link = f'[COL {i}](https://github.com/BenjaminHalko/BenjaminHalko/issues/new?title=Connect4:+{i}&body=Please+do+not+change+the+title.+Just+click+"Submit+new+issue".+You+do+not+need+to+do+anything+else.+%3AD)'
            value += f'| {link} '
        value += '|\n' + '| :-: ' * 8 + '|\n'

        for j in range(6):
            value += '|'
            for i in range(8):
                value += f' <img src="https://github.com/BenjaminHalko/BenjaminHalko/raw/main/games/{imgs[data["board"][i][j]+1]}" alt="{imgs[data["board"][i][j]+1].split("/")[1].split(".")[0]}" width="50px"> |'
            value += '\n'

        # Update stats
        stats = {
            "Red Wins": data["games_won"][0],
            "Yellow Wins": data["games_won"][1]
        }

        if data["games_won"][2] > 0:
            stats["Draws"] = data["games_won"][2]

        if len(data["game_times"]) > 0:
            stats["Average Time per Game"] = format_time(sum(data["game_times"]) / len(data["game_times"]))
            stats["Average Moves per Game"] = sum(data["game_moves"]) / len(data["game_moves"])

        info = f"<b>A game of Connect 4 played on GitHub.</b><br>{dot} Click on a column to make a move. It is currently {color}'s turn. {dot}"
        if "game_over" in data:
            info = f"<b>A game of Connect 4 played on GitHub.</b><br>The game is currently over. {currentWinner}<br>Click on a column to start a new game."

        updateReadme("Connect 4","CONNECT4",info,value, data["leaderboard"], data["history"],stats)

        # Create comment
        issue.create_comment(f"@{user} Thanks for playing Connect 4! See the readme for the updated board.")
        issue.edit(state="closed", labels=[previousColor])
    except Exception as e:
        issue.create_comment("Sorry, something went wrong. Please try again.")
        issue.edit(state="closed", labels=['Invalid'])
        sys.exit(1)