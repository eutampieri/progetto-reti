#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
from json import loads
from tkinter import messagebox

"""La funzione che segue ha il compito di gestire la ricezione dei messaggi."""


def receive():
    while True:
        try:
            # quando viene chiamata la funzione receive, si mette in ascolto dei messaggi che
            # arrivano sul socket
            try:
                msg = loads(client_socket.recv(BUFSIZ).decode("utf8"))
                print(msg)
            except:
                continue
            if msg["action"] == "send_message":
                tkt.messagebox.showinfo(
                    title="CoolNetGame", message=msg["message"])
            elif msg["action"] == "scoreboard":
                for i, x in enumerate(msg["board"]):
                    if x["is_me"]:
                        tkt.messagebox.showinfo(title="CoolNetGame Scoreboard", "You're "+str(x["score"] + "th!"))
            elif msg["action"] == "choose":
                question.configure(text=msg["message"])
                ans0["text"] = msg["options"][0][1]
                ans1["text"] = msg["options"][1][1]
                ans2["text"] = msg["options"][2][1]
            elif msg["action"] == "quit":
                tkt.messagebox.showerror(
                    "The game will now close", message=msg["reason"])
                on_closing()
            else:
                print(msg)
        except OSError:
            break


"""La funzione che segue viene invocata quando viene chiusa la finestra della chat."""


def on_closing(event=None):
    client_socket.close()
    finestra.destroy()


def send(msg):
    client_socket.send(bytes(msg, "utf8"))


def send0(event=None):
    send("0")


def send1(event=None):
    send("1")


def send2(event=None):
    send("2")


def send_ready(event=None):
    send("ready")
    ready["state"] = "disable"


finestra = tkt.Tk()
finestra.title("Chat_Laboratorio")

question = tkt.Label(finestra)

ans0 = tkt.Button(finestra, command=send0)
ans1 = tkt.Button(finestra, command=send1)
ans2 = tkt.Button(finestra, command=send2)

ready = tkt.Button(finestra, text="Ready?", command=send_ready)

question.pack()
ans0.pack()
ans1.pack()
ans2.pack()
ready.pack()

finestra.protocol("WM_DELETE_WINDOW", on_closing)

# ----Connessione al Server----
HOST = input('Inserire il Server host: ')
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.send(bytes("api", "utf-8"))

receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra Chat.
tkt.mainloop()
