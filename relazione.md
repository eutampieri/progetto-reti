# Relazione Progetto
## Traccia 3 - CHATGAME
Michael Chelli   0000915585

Eugenio Tampieri 0000915602

June 2021

## Introduzione
Il progetto consinte nel realizzare un programma con il linguaggio Python che permetta di giocare a un chat game sulla rete.

## Descrizione

Il gioco prevede di inviare agli utenti connessi delle domande. Rispondendo correttamente si guadagnano punti, altrimenti se ne perdono.

Riteniamo la compatibilità una caratteristica importante, per questo motivo abbiamo deciso di implementare sia un'interfaccia testuale, utilizzabile da un'ampia gamma di dispositivi ad es. utilizzando il comando `telnet` o `nc`, che l'invio di messaggi ai client in formato JSON, attivabile inviando `api` entro 500 ms dalla connessione, particolarmente adatta se si vogliono sviluppare dei client grafici.

### Server

Il server non è implementato in un singolo file, ma in piu file tutti dentro la cartella server.

Una volta lanciato il server, eseguendo `python3 server/server.py` rimarrà in attesa di connessioni sulla porta TCP 53000, effettuando un binding su tutte le interfacce disponibili.

Quando un client si connette, gli viene assegnato un nome e viene aggiunto alla lista dei giocatori.

Appena connesso il client riceverà una guida su come operare.

Quando piu della meta dei client connessi hanno inviato il comando `ready` per dichiarare che sono pronti ad iniziare il gioco,
il gioco ha inizio e il server smette di accettare nuove connessioni.

Nella durata di 5 minuti viene effettuato il gioco.

Il gioco dura tanti turni quanto un giocatore riesce ad andare avanti entro il tempo limite.

Ogni turno viene posta una scelta ceca al giocatore con 3 possibilità in cui se sbaglia viene eliminato e disconnesso dopo aver ricevuto la classifica corrente.

Se invece non sbaglia, gli viene posta una domanda con 3 possibilità, se risponde correttamente gli viene assegnato +1 punto, altrimenti -1 punto.

Se il tempo limite non è ancora terminato, il giocatore passa al prossimo turno.

Alla fine del gioco, verra mandata una scoreboard al giocatore e verrà disconnesso dal server, che finirà l'esecuzione.

### Client

In questo repo sono presenti due client:

 - Uno, realizzato in Python tramite la libreria `tkinter`, eseguibile tramite `python3 client.py`
 - Un altro, realizzato in HTML5+JS+CSS3, che invece sfrutta i WebSocket.

Per la webapp è stato realizzato un proxy che si connette al server tramite una connessione TCP ed espone i messaggi JSON su un WebSocket sulla porta 8080.

Pertanto, per utilizzare la webapp è necessario avere installata la [toolchain Rust](https://www.rust-lang.org/tools/install),
necessaria a compilare il proxy WebSocket. Per compilarla ed eseguirla, lanciare dalla directory `proxy`
il comando `cargo run --release 127.0.0.1 53000`, assumendo che il server sia in esecuzione sulla stessa
macchina sulla porta TCP 53000.

Il client, che può essere eseguito su qualsiasi HTTP server, chiederà all'avvio l'indirizzo del WebSocket. Quello di default
è coerente con i passi indicati in questa relazione, pertanto non dovrebbe essere modificato.

### Comandi disponibili
- Subito dopo la connessione
	- api: abilita la modalità api
- In fase di waiting
	- ready: dichiara di essere pronto a giocare
- In fase di gioco
	- 0|1|2: rispondi 0 o 1 o 2 all'ultima domanda
	- quit: abbandona la partita
	- setname _newname_: cambia nome

### Documentazione messaggi JSON

Esistono quattro tipi di messaggi:
1. `send_message`, utilizzato per inviare notifiche al client
   ```json
   {"action": "send_message", "message": "the message to be displayed"}
   ```
1. `quit`, per segnalare al client che deve chiudere il socket e terminare l'esecuzione
   ```json
   {"action": "quit", "reason": "The game has ended"}
   ```
1. `choose`, per chiedere al client di scegliere fra più opzioni
   ```json
   {
	   "action": "choose",
	   "message": "prompt the user to choose a message",
	   "options": [ // An array of options
		   [] // An option. The first element is the payload to send to the server,
		      // while the second element is the text to show to the user, i.e.
			  // the question
	   ]
   }
   ```
1. `scoreboard`, per chiedere al client di mostrare la classifica
   ```json
   {
	   "action": "scoreboard",
	   "board": [ // An entry for each player
		   {
			   "name": "Alice",
			   "score": 3,
			   "is_me": true // Wether or not the current entry represent the score of the player using the connected client
		   }
	   ]
   }
   ```

## Dettagli implementativi
La scelta delle domande viene effettuata casualmente utilizzando [raw.githubusercontent.com/deepmind/AQuA/master/test.json](questo dataset)
che viene scaricato tramite http quando viene lanciato il server.

La comunicazione server-client puo essere effettuata in 2 modalità: normale e api.

La modalità api codifica i messaggi in json, mentre la modalità normale serve per i client testuali.

La modalità api viene attivata se il comando 'api' viene inviato al server entro 0.5s dalla connessione del client.

La comunicazione client-server, essendo molto semplice, avviene sempre in forma testuale.

Il server di gioco, oltre al thread principale, utilizza: un thread per accettare le connessioni, un thread per gestire il gioco e un thread per ogni client.

### Tampieri

Io mi sono occupato di realizzare il client Tkinter, un semplice client HTTPS
(utilizzato per scaricare il dataset), la modalità di invio dei messaggi tramite
JSON, la webapp ed il proxy per WebSocket.

Ho trovato interessante soprattutto lo sviluppo del client HTTPS, situato in `server/http_client.py`,
perché, nonostante sia semplice inviare una richiesta `GET` ad un server HTTP, mi sono imbattuto in
diversi problemi:
- Il server di GitHub, su cui è hostato il dataset, non supporta HTTP 1.0 e richiede l'invio dell'header
  `Host`
- Il server di GitHub richiede l'utilizzo di HTTPS, così ho avuto modo di approfondire la creazione di
  wrapped sockets per poter utilizzare SSL
- Il server mantiene la connessione aperta dopo aver finito di inviare il file (bisognerebbe vedere se
  con `Connection: Close` si riuscisse ad ovviare al problema), perciò inizialmente effettuavo il parsing
  di `Content-Length`, ma poi ho trovato più semplice controllare che non venissero inviati nuovi bytes.

Altra cosa per me proficua è stato l'utilizzo dei WebSocket, che non avevo mai avuto occasione di usare.

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

Il sorgente di questo progetto è presente al seguente link https://github.com/eutampieri/progetto-reti

