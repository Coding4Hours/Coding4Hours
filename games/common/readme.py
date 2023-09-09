def format_leaderboard(leaderboard):
    top_moves = sorted([[moves, user] for user, moves in leaderboard.items()], key=lambda x: -x[0])
    value = "| Moves | User |\n| :-: | :-: |\n"
    for moves, user in top_moves[:10]:
        value += f"| {moves} | [ @{user}](https://github.com/{user}) |\n"
    return value

def format_history(history):
    value = "| Move | User |\n| :-: | :-: |\n"
    for moves, user in history:
        value += f"| {moves} | [ @{user}](https://github.com/{user}) |\n"
    return value

def format_stats(stats):
    value = "| Stat | Value |\n| :-: | :-: |\n"
    for stat, val in stats.items():
        value += f"| {stat} | {val} |\n"
    return value

def format_time(time):
    days = time // 86400
    time = time % 86400
    hours = time // 3600
    time = time % 3600
    minutes = time // 60
    time = time % 60
    seconds = time

    string = ""
    if days > 0:
        string += f"{int(days)} Days, "
    if hours > 0:
        string += f"{int(hours)} Hours, "
    if minutes > 0:
        string += f"{int(minutes)} Minutes, "
    string += f"{int(seconds)} Seconds"
    return string

def updateReadme(name, ID, info, board, leaderboard, history, stats, moves=""):
    readme = ""
    with open("README.md", "r") as f:
        readme = f.read()
    readme = readme.split(f"<!-- {ID} -->\n")
    readme[1] = f"""<details align="center"><summary><h2>{name}</h2></summary>
<table align="center">
<tr></tr>
<tr><td>
<p align="center">{info}</p><p>

{board}
{moves}
<details align="left"><summary><h3>History of moves for this game</h3></summary>

{format_history(history)}
</details>

<details align="left"><summary><h3>Top 10 most active players</h3></summary>

{format_leaderboard(leaderboard)}
</details>

<details align="left"><summary><h3>Stats</h3></summary>

{format_stats(stats)}
</details>
</td></tr>
</table>
</details>
"""
    readme = f"<!-- {ID} -->\n".join(readme)
    with open("README.md", "wb") as f:
        f.write(readme.encode("utf-8"))