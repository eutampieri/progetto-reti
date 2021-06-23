function connect(server, username) {
    var ws = new WebSocket(server);
    ws.send("setname " + username.replace(/\s/g, ""));
    return ws;
}

function run(ws) {
    ws.onmessage = function (event) {
        try {
            var message = JSON.parse(event.data);
            switch (message.action) {
                case "message":
                    alert(message.message);
                    break;

            }
        } catch (e) { }
    }
}