#!/usr/bin/env python3
"""Game server"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

""" Handle incoming connections"""
def handle_incoming():
    while True:
        client, client_address = SERVER.accept()
        print("[_] New client (%s:%s)" % client_address)
        #al client che si connette per la prima volta fornisce alcune indicazioni di utilizzo
        client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
        # ci serviamo di un dizionario per registrare i client
        addrs[client] = client_address
        #diamo inizio all'attività del Thread - uno per ciascun client
        Thread(target=handle_client, args=(client,)).start()
        

"""Handle a single client connection."""
def handle_client(client):  # Prende il socket del client come argomento della funzione.
    nome = client.recv(BUFSIZ).decode("utf8")
    #da il benvenuto al client e gli indica come fare per uscire dalla chat quando ha terminato
    welcome_msg = 'Welcome %s! If you want to leave the game, type {quit} to quit.' % nome
    client.send(bytes(welcome_msg, "utf8"))
    msg = "%s joined the game!" % nome
    #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
    broadcast(bytes(msg, "utf8"))
    #aggiorna il dizionario clients creato all'inizio
    clients[client] = nome
    
#si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, nome+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s left the game." % nome, "utf8"))
            break

""" Send a broadcast message."""
def broadcast(msg, prefix=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addrs = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=handle_incoming)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
