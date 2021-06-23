function connect(server, username) {
    var ws = new WebSocket(server);
    ws.onopen = function (x) {
        ws.send("setname " + username.replace(/\s/g, ""));
    }
    return ws;
}

function run(ws) {
    ws.onmessage = function (event) {
        try {
            var message = JSON.parse(event.data);
            switch (message.action) {
                case "send_message":
                    alert(message.message);
                    break;
                case "choose":
                    document.getElementById("choose_title").innerHTML = message.message;
                    var choices = document.getElementById("choices");
                    choices.innerHTML = "";
                    for (var i = 0; i < message.options.length; i++) {
                        var el = document.createElement("button");
                        el.onclick = function () {
                            ws.send(message.options[i][0]);
                        };
                        el.innerHTML = message.options[i][1];
                        choices.appendChild(el);
                    }
                    break;
                default:
                    console.log(event.data)
                    break;

            }
        } catch (e) {
            console.error(e);
            console.log(event.data)
        }
    }
}