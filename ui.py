from json import dumps

"""Returns a dict of functions that return the message"""


def get_messages(is_api):
    if is_api:
        return {
            "message": lambda x: dumps({"action": "send_message", "message": x}),
            "quit": lambda x: dumps({"action": "quit", "reason": x}),
            "choose": lambda x: dumps({"action": "choose", "message": x[0], "options": x[1]}),
        }
    else:
        return {
            "message": lambda x: x + "\n",
            "quit": lambda x: "Bye bye! " + x + "\n",
            "choose": lambda x: x[0] + "\n" + "\n".join([item[0] + ":\t" + item[1] for item in x[1]]) + "\n",
        }
