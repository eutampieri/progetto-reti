#!/usr/bin/env python3
"""Game server"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from game import get_question, get_random_mapping
from ui import get_messages
import time
import signal
import sys

USAGE = """
While waiting for a game to start, you can type 'ready' to ready up.
When more than half of the connected players is ready, the game starts.
To answer to the questions type either '0', '1' or '2'.
To change username, type 'setname <new_username>' note that no spaces are allowed in usernames.
To quit the game, type 'quit'.

The game will last for 300s, during which you should try to answer to as many questions correctly.

Before every question you will be asked to pick a number between 0 and 2,
if you pick the wrong one, the game will end for you.

Every question has 3 possible answers,
if you pick the correct one you will be awarded +1 points,
if you pick the wrong one you will be awarded -1 points,
note that your score can become negative.

"""

HOST = '0.0.0.0'
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

GAME_DURATION = 300
WAITING = 0
IN_GAME = 1
OVER = 2

state = WAITING
players = []
num_connected_clients = 0
num_ready_clients = 0

all_threads = []

class Player:
	def __init__(self, client, address, player_id, name, is_api):
		self.client = client
		self.address = address
		self.player_id = player_id
		self.name = name
		self.score = 0
		self.is_api = is_api
		self.to_close = False
		self.is_ready = False
	def msg(self, msg):
		try:
			self.client.send(bytes(msg, "utf8"))
		except:
			self.close("Some communication error occurred")
	def close(self, msg):
		global num_connected_clients
		time.sleep(1)
		if not self.to_close:
			msgs = get_messages(self.is_api)
			self.msg(msgs["scoreboard"]((players, self)))
			self.msg(msgs["quit"](msg))
			num_connected_clients -= 1
			self.to_close = True
		try:
			self.client.close()
		except:
			return


def accept_loop():
	global state
	global num_connected_clients
	global num_ready_clients
	global all_threads
	# handle incoming connections
	while state == WAITING:
		try:
			client, client_address = SERVER.accept()
		except ConnectionAbortedError:
			break
		print("[_] New client (%s:%s)" % client_address)

		client_id = num_connected_clients
		name = "Player" + str(client_id)
		bad_name = True
		while bad_name:
			name = name+"_"
			bad_name = False
			for i in players:
				if i.name == name:
					bad_name = True
					break

		# check if API
		api = False
		client.settimeout(0.5)
		try:
			msg = client.recv(BUFSIZ).decode("utf-8")
			if msg.strip() == "api":
				api = True
		except:
			pass
		client.settimeout(GAME_DURATION)

		player = Player(client, client_address, client_id, name, api)
		players.append(player)

		# diamo inizio all'attività del Thread - uno per ciascun client
		t = Thread(target=handle_client, args=(player,))
		t.daemon = True
		all_threads.append(t)
		t.start()
		num_connected_clients += 1

def main_loop():
	global state
	global num_connected_clients
	global num_ready_clients

	while state == WAITING:
		time.sleep(1)
		if num_ready_clients*2 > num_connected_clients:
			state = IN_GAME

	# Game loop
	print("Entering game")
	time.sleep(GAME_DURATION)
	state = OVER
	print(players)


def get_response(player):
	global num_ready_clients

	msgs = get_messages(player.is_api)

	while True:
		try:
			ans = player.client.recv(BUFSIZ).decode("utf8").strip().split()
		except:
			player.close("Some communication error occurred")
			break


		if len(ans) == 0:
			continue

		elif len(ans) == 2 and ans[0] == "setname":
			name = ans[1]
			bad_name = False
			for i in players:
				if i.name == name:
					bad_name = True
					player.msg(msgs["message"]("This name is already in use, please select another name"))
					break
			if not bad_name:
				player.name = name
				player.msg(msgs["message"]("You changed name to %s" % name))

		elif len(ans) == 1 and ans[0] == "quit":
			player.close("You quit the game")
			break

		elif len(ans) == 1 and ans[0].isdigit():
			res = int(ans[0])
			if res == 0 or res == 1 or res == 2:
				return res
		else:
			player.msg(msgs["message"]("Unknown command"))


"""Handle a single client connection."""
# prende il socket del client come argomento della funzione.
def handle_client(player):
	global state
	global num_ready_clients

	# send usage guide
	player.msg(USAGE)

	# send welcome message
	player.msg("You joined the game with name %s\n" % player.name)

	msgs = get_messages(player.is_api)

	while state == WAITING:
		if player.is_ready:
			player.msg(msgs["message"]("Waiting for game to start ({}/{} players ready)".format(num_ready_clients, num_connected_clients)))
			time.sleep(2)
		else:
			player.client.settimeout(4)
			try:
				player.msg(msgs["message"]("type 'ready' to ready up! ({}/{} players ready)".format(num_ready_clients, num_connected_clients)))
				msg = player.client.recv(BUFSIZ).decode("utf-8")
				if msg.strip() == "ready":
					player.is_ready = True
					num_ready_clients += 1
					player.msg(msgs["message"]("Readyd up"))
			except:
				pass
			player.client.settimeout(GAME_DURATION)

	player.msg(msgs["message"]("Game started!"))
	turn = 0
	while state == IN_GAME:
		player.msg(msgs["choose"](("Choose a question:", [(str(i), "Question " + chr(ord('A') + i)) for i in range(3)])))
		ans = get_response(player)
		if player.to_close:
			break
		is_bad, question = get_question(turn, ans)
		if is_bad:
			player.close("Your choice was the trap, you lost!")
			break

		player.msg(msgs["choose"]((question[0], [(str(i[0]), i[1]) for i in enumerate(question[1])])))

		ans = get_response(player)
		if player.to_close:
			break
		if ans == question[2]:
			player.msg(msgs["message"]("Your answer was correct! You get a point"))
			player.score += 1
		else:
			player.msg(msgs["message"]("Your answer was wrong! You lose a point"))
			player.score -= 1
		turn += 1
	player.close("The game is over")

""" Send a broadcast message."""
# il prefisso è usato per l'identificazione del nome.
def broadcast(msg):
	global players
	for utente in players:
		utente.msg(msg)



def signal_handler(signal, frame):
	print("exiting")
	state = OVER
	for i in players:
		i.close("The session was terminated by the server")
	SERVER.close()
	sys.exit(0)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)

	SERVER.listen(5)
	print("In attesa di connessioni...")
	ACCEPT_THREAD = Thread(target=accept_loop)
	MAIN_THREAD = Thread(target=main_loop)
	ACCEPT_THREAD.daemon = True
	MAIN_THREAD.daemon = True
	all_threads.append(ACCEPT_THREAD)
	all_threads.append(MAIN_THREAD)

	ACCEPT_THREAD.start()
	MAIN_THREAD.start()

	for t in all_threads:
		t.join()

	state = OVER
	for i in players:
		i.close("The game is over")
	SERVER.close()
