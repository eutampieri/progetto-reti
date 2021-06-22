#!/usr/bin/env python3
"""Game server"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from game import get_question
import time

class Player:
	def __init__(self, client, address, player_id, name, is_api):
		self.client = client
		self.address = address
		self.player_id = player_id
		self.name = name
		self.score = 0
		self.is_api = is_api

WAITING = 0
IN_GAME = 1
OVER = 2
state = WAITING
players = []

def main_loop():
	global state
	num_connected_clients = 0
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
					client.send(bytes("This name is already in use, please select another name\n", "utf8"))
					break
		# send welcome message
		client.send(bytes("You joined the game with name %s\n" % name, "utf8"))

		#check if API
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
		if num_connected_clients >= 2:
			state = IN_GAME

	# Game loop
	print("Entering game")
	time.sleep(60)
	state = OVER
	print(players)

"""Handle a single client connection."""
def handle_client(client_id):  # prende il socket del client come argomento della funzione.
	global state
	client = players[client_id].client
	name = players[client_id].name
	
	client.send(bytes("Waiting for game to start...\n","utf8"))
	while state == WAITING:
		time.sleep(1)
	
	client.send(bytes("Game started!\n", "utf8"))
	turn = 0
	while state == IN_GAME:
		ans = 0
		while True:
			client.send(bytes("Choose a question from 0 to 2\n", "utf8"))
			ans = client.recv(BUFSIZ).decode("utf8").strip()
			if ans == "0" or ans == "1" or ans == "2":
				ans = int(ans)
				break
		is_bad, question = get_question(turn,ans)
		if is_bad:
			client.send(bytes("Your choice was the trap, you lost!\n","utf-8"))
			break
		
		client.send(bytes(question[0]+"\n","utf-8"))
		for i in range(3):
			client.send(bytes(str(i)+") "+question[1][i]+"\n","utf-8"))
		
		ans = 0
		while True:
			client.send(bytes("Choose an answer from 0 to 2\n", "utf8"))
			ans = client.recv(BUFSIZ).decode("utf8").strip()
			if ans == "0" or ans == "1" or ans == "2":
				ans = int(ans)
				break
		if ans == question[2]:
			client.send(bytes("Your answer was correct! You get a point\n","utf-8"))
			players[client_id].score += 1
		else:
			client.send(bytes("Your answer was wrong! You lose a point\n","utf-8"))
			players[client_id].score -= 1
		turn += 1

""" Send a broadcast message."""
def broadcast(msg, prefix=""):	# il prefisso è usato per l'identificazione del nome.
	for utente in clients:
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
	ACCEPT_THREAD = Thread(target=main_loop)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
