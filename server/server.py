#!/usr/bin/env python3
"""Game server"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from game import get_question, get_random_mapping
from ui import get_messages
import time

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


WAITING = 0
IN_GAME = 1
OVER = 2
state = WAITING
players = []
num_connected_clients = 0
num_ready_clients = 0

def accept_loop():
	global state
	global num_connected_clients
	global num_ready_clients
	# handle incoming connections
	while state == WAITING:
		client, client_address = SERVER.accept()
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
		# send welcome message
		client.send(bytes("You joined the game with name %s\n" % name, "utf8"))

		# check if API
		api = False
		client.settimeout(1)
		try:
			msg = client.recv(BUFSIZ).decode("utf-8")
			if msg.strip() == "api":
				api = True
		except:
			pass
		client.settimeout(None)

		players.append(Player(client, client_address, client_id, name, api))

		# diamo inizio all'attività del Thread - uno per ciascun client
		Thread(target=handle_client, args=(client_id,)).start()
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
	time.sleep(60)
	state = OVER
	print(players)

def close_client(client_id):
	global num_connected_clients
	players[client_id].to_close = True
	num_connected_clients -= 1
	try:
		players[client_id].client.close()
	except:
		return
	
def get_response(client_id):
	global num_ready_clients
	
	client = players[client_id].client
	msgs = get_messages(players[client_id].is_api)
	
	while True:
		try:
			ans = client.recv(BUFSIZ).decode("utf8").strip().split()
		except:
			close_client(client_id)
			break
			

		if len(ans) == 0:
			continue
		
		elif len(ans) == 2 and ans[0] == "setname":
			name = ans[1]
			bad_name = False
			for i in players:
				if i.name == name:
					bad_name = True
					client.send(bytes(msgs["message"]("This name is already in use, please select another name"), "utf8"))
					break
			if not bad_name:
				players[client_id].name = name
				client.send(bytes(msgs["message"]("You changed name to %s" % name), "utf8"))


		elif len(ans) == 1 and ans[0] == "quit":
			client.send(bytes(msgs["quit"]("You quit the game"), "utf-8"))
			close_client(client_id)
			break

		elif len(ans) == 1 and ans[0].isdigit():
			res = int(ans[0])
			if res == 0 or res == 1 or res == 2:
				return res
		else:
			client.send(bytes(msgs["message"]("Unknown command"), "utf8"))
	

"""Handle a single client connection."""
# prende il socket del client come argomento della funzione.
def handle_client(client_id):
	global state
	global num_ready_clients

	client = players[client_id].client
	name = players[client_id].name

	msgs = get_messages(players[client_id].is_api)

	while state == WAITING:
		if players[client_id].is_ready:
			client.send(bytes(msgs["message"]("Waiting for game to start..."), "utf8"))
			time.sleep(1)
		else:
			client.settimeout(4)
			try:
				client.send(bytes(msgs["message"]("type 'ready' to ready up!"), "utf8"))
				msg = client.recv(BUFSIZ).decode("utf-8")
				if msg.strip() == "ready":
					players[client_id].is_ready = True
					num_ready_clients += 1
					client.send(bytes(msgs["message"]("Readyd up"), "utf8"))
			except:
				pass
			client.settimeout(None)

	client.send(bytes(msgs["message"]("Game started!"), "utf8"))
	turn = 0
	while state == IN_GAME:
		client.send(bytes(msgs["choose"](("Choose a question:", [(str(i), "Question " + chr(ord('A') + i)) for i in range(3)])), "utf8"))
		ans = get_response(client_id)
		if players[client_id].to_close:
			break
		is_bad, question = get_question(turn, ans)
		if is_bad:
			client.send(bytes(msgs["quit"]("Your choice was the trap, you lost!"), "utf-8"))
			close_client(client_id)
			break

		client.send(bytes(msgs["choose"](
			(question[0], [(str(i[0]), i[1]) for i in enumerate(question[1])])), "utf-8"))

		ans = get_response(client_id)
		if players[client_id].to_close:
			break
		if ans == question[2]:
			client.send(bytes(msgs["message"]("Your answer was correct! You get a point"), "utf-8"))
			players[client_id].score += 1
		else:
			client.send(bytes(msgs["message"]("Your answer was wrong! You lose a point"), "utf-8"))
			players[client_id].score -= 1
		turn += 1

""" Send a broadcast message."""
# il prefisso è usato per l'identificazione del nome.
def broadcast(msg, prefix=""):
	global players
	for utente in players:
		utente.send(bytes(prefix, "utf8")+msg)


HOST = 'localhost'
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
	SERVER.listen(5)
	print("In attesa di connessioni...")
	ACCEPT_THREAD = Thread(target=accept_loop)
	MAIN_THREAD = Thread(target=main_loop)
	ACCEPT_THREAD.start()
	MAIN_THREAD.start()
	try:
		MAIN_THREAD.join()
	except KeyboardInterrupt:
		pass
	finally:
		#TODO @MyK00l close all clients
		SERVER.close()
