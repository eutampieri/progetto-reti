from json import dumps

"""Returns a dict of functions that return the message"""


def get_scoreboard(x):
    points_names = [(y.score, "** " + y.name + " **" if y.player_id ==
                     x[1].player_id else y.name) for y in x[0]]
    points_names.sort()
    return "Here's the current scoreboard:\n" + "\n".join([str(i+1) + "\t" + x[1] + " (" + x[0] + " points)" for i, x in enumerate(points_names)])


def get_messages(is_api):
    if is_api:
        return {
            "message": lambda x: dumps({"action": "send_message", "message": x}),
            "quit": lambda x: dumps({"action": "quit", "reason": x}),
            "choose": lambda x: dumps({"action": "choose", "message": x[0], "options": x[1]}),
            "scoreboard": lambda x: dumps({"action": "scoreboard", "board": [{"name": y.name, "score": y.score, "is_me": y.player_id == x[1].player_id} for y in x[0]]}),
        }
    else:
        return {
            "message": lambda x: x + "\n",
            "quit": lambda x: "Bye bye! " + x + "\n",
            "choose": lambda x: x[0] + "\n" + "\n".join([item[0] + ":\t" + item[1] for item in x[1]]) + "\n",
            "scoreboard": lambda x: get_scoreboard(s) + "\n",
        }
