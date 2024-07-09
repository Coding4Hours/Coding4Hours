import sys
from common.readme import updateReadme, format_time
from common.issue import GetInfo
from common.data import load_common_data, save_data

# Load data
def load_data():
    data, gameOver = load_common_data("games/ttt_data/data.json")

    if "board" not in data or gameOver:
        data["board"] = [[-1] * 6 for i in range(8)]
        print("New board created")

    return data

# Make a move
def make_move():
    board = data["board"]
    move = get_move()
        
# Get move
def get_move():
    if issue.title.lower().startswith("connect4:"):
        return int(issue.title.split(":")[1].split(' ')[-1])
    return -1

# master
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
        save_data(data, state, user, "games/ttt_data/data.json")

        # Update readme
        color = "X" if nextTurn == 0 else "O"
        dot = 'X' if nextTurn == 0 else 'O' 

        # Create Board
        imgs = ['common/blank.png', 'ttt_data/x.png', 'ttt_data/o.png']
        value = ''
        for i in range(3):
            link = f'{i}'
            if data["board"][i][0] == -1:
                link = f'[COL {i}](https://github.com/Coding4Hours/Coding4Hours/issues/new?title=Tic Tac Toe:+{i}&body=Please+do+not+change+the+title.+Just+click+"Submit+new+issue".+You+do+not+need+to+do+anything+else.+%3AD)'
            value += f'| {link} '
        value += '|\n' + '| :-: ' * 3 + '|\n'

        for j in range(3):
            value += '|'
            for i in range(8):
                value += f' <img src="https://github.com/Coding4Hours/Coding4Hours/raw/master/games/{imgs[data["board"][i][j]+1]}" alt="{imgs[data["board"][i][j]+1].split("/")[1].split(".")[0]}" width="50px"> |'
            value += '\n'

        # Update stats
        stats = {
            "X Wins": data["games_won"][0],
            "O Wins": data["games_won"][1]
        }

        if data["games_won"][2] > 0:
            stats["Draws"] = data["games_won"][2]

        if len(data["game_times"]) > 0:
            stats["Average Time per Game"] = format_time(sum(data["game_times"]) / len(data["game_times"]))
            stats["Average Moves per Game"] = sum(data["game_moves"]) / len(data["game_moves"])

        info = f"<b>A game of Connect 4 played on GitHub.</b><br>{dot} Click on a column to make a move. It is currently {color}'s turn. {dot}"
        if "game_over" in data:
            info = f"<b>A game of Connect 4 played on GitHub.</b><br>The game is currently over. {currentWinner}<br>Click on a column to start a new game."

        updateReadme("Tic Tac Toe","TICTACTOE",info,value, data["leaderboard"], data["history"],stats)

        # Create comment
        issue.create_comment(f"@{user} Thanks for playing Connect 4! See the readme for the updated board.")
        issue.edit(state="closed", labels=[previousColor])
    except Exception as e:
        issue.create_comment("Sorry, something went wrong. Please try again.")
        issue.edit(state="closed", labels=['Invalid'])
        sys.exit(1)
