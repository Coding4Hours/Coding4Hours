import json
from os import path
import time

def load_common_data(file):
    if path.exists(file):
        with open(file, "r") as f:
            data = json.load(f)
    else:
        data = {}

    gameOver = "game_over" in data

    if "turn" not in data:
        data["turn"] = 0

    if "games_won" not in data:
        data["games_won"] = [0, 0, 0]

    if "leaderboard" not in data:
        data["leaderboard"] = {}

    if "history" not in data or gameOver:
        data["history"] = []

    if "game_times" not in data:
        data["game_times"] = []
    
    if "game_moves" not in data:
        data["game_moves"] = []

    if "game_start_time" not in data or gameOver:
        data["game_start_time"] = time.time()

    if gameOver:
        data.pop("game_over")

    return data, gameOver

def save_data(data, state, user, file):
    if state == "win" or state == "draw":
        data["game_over"] = True
        data["game_times"].append(time.time() - data["game_start_time"])
        data["game_moves"].append(len(data["history"]))
        if state == "win":
            data["games_won"][data["turn"]] += 1
        else:
            data["games_won"][2] += 1
    data["turn"] = 1 - data["turn"]
    if user not in data["leaderboard"]:
        data["leaderboard"][user] = 1
    else:
        data["leaderboard"][user] += 1

    with open(file, "w") as f:
        json.dump(data, f, indent=4)