# Relazione Progetto
## Traccia 3 - CHATGAME
Michael Chelli   0000915585
Eugenio Tampieri 0000915602
June 2021

## Introduzione
Il progetto consinte nel realizzare un programma con il linguaggio Python che permetta di giocare a un chat game sulla rete.

## Descrizione
Sebbene il gioco sia perfettamente utilizzabile con il comando telnet,
Abbiamo deciso di aggiungere anche un api in modo da poter facilmente costruire client personalizzati
come client.py.
Sono quindi presenti nella repo 2 programmi utilizzabili:
- server/server.py
- client.py
entrambi eseguibili con python3.
Il server non e' implementato in un singolo file, ma in piu file tutti dentro la cartella server.

Una volta eseguito il server rimarra' in attesa di connessioni sulla porta 53000.
Quando un client si connette, gli viene assegnato un nome e viene aggiunto alla lista dei giocatori.
Appena connesso il client ricevera' una guida su come operare.
Quando piu della meta dei client connessi hanno inviato il comando 'ready' per dichiarare che sono pronti ad iniziare il gioco,
parte il gioco e il server smette di accettare nuove connessioni.
Nella durata di 60 minuti viene effettuato il gioco.
Il gioco dura tanti turni quanto un giocatore riesce ad andare avanti entro il tempo limite.
Ogni turno viene posta una scelta ceca al giocatore con 3 possibilita' in cui se sbaglia viene eliminato e disconnesso dopo aver ricevuto la classifica corrente.
Se invece non sbaglia, gli viene posta una domanda con 3 possibilita', se risponde correttamente gli viene assegnato +1 punto, altrimenti -1 punto.
Se il tempo limite non e' ancora terminato, il giocatore passa al prossimo turno.
Alla fine del gioco, verra mandata una scoreboard al giocatore e verra' disconnesso dal server, che finira' l'esecuzione.

### Comandi disponibili
- Subito dopo la connessione
	- api: abilita la modalita' api
- In fase di waiting
	- ready: dichiara di essere pronto a giocare
- In fase di gioco
	- 0|1|2: rispondi 0 o 1 o 2 all'ultima domanda
	- quit: abbandona la partita
	- setname <newname>: cambia nome

## Dettagli implementativi
La scelta delle domande viene effettuata casualmente utilizzando [raw.githubusercontent.com/deepmind/AQuA/master/test.json](questo dataset)
che viene scaricato tramite http quando viene lanciato il server.

La comunicazione server-client puo essere effettuata in 2 modalita': normale e api.
La modalita' api codifica i messaggi in json, mentre la modalita' normale serve per i client testuali.
La modalita' api viene attivata se il comando 'api' viene inviato al server entro 0.5s dalla connessione del client.
La comunicazione client-server essendo molto semplice avviene sempre in forma testuale.

Il server di gioco oltre al thread principale, utilizza: un thread per accettare le connessioni, un thread per gestire il gioco e un thread per ogni client.


## Librerie utilizzate
- socket
- threading
- time
- signal
- sys
- json
- random
- ssl
- tkinter (solo per il client con GUI in python)

Il sorgente di questo progetto e' presente al seguente link https://github.com/eutampieri/progetto-reti

