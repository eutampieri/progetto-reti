var Game = {
    ws: null,
    connect: function (server, username) {
        this.ws = new WebSocket(server);
        this.ws.onopen = function (x) {
            Game.changeName(username);
        }
    },

    run: function () {
        this.ws.onmessage = function (event) {
            try {
                var message = JSON.parse(event.data);
                switch (message.action) {
                    case "send_message":
                        alert(message.message);
                        break;
                    case "choose":
                        document.getElementById("choose_view").classList.remove("d-none");
                        document.getElementById("choose_title").innerHTML = message.message;
                        var choices = document.getElementById("choices");
                        choices.innerHTML = "";
                        for (var i = 0; i < message.options.length; i++) {
                            var el = document.createElement("button");
                            el.type = "button";
                            el.className = "d-block btn btn-primary";
                            var toSend = message.options[i][0];
                            el.onclick = function () {
                                Game.ws.send(toSend);
                            };
                            el.innerHTML = message.options[i][1];
                            choices.appendChild(el);
                        }
                        break;
                    case "quit":
                        document.getElementById("choose_view").classList.add("d-none");
                        alert("You were kicked from the game :(\n" + message["reason"]);
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
    },

    "ready": function (btn) {
        btn.classList.add("d-none");
        Game.ws.send("ready");
    },

    changeName: function (name) {
        this.ws.send("setname" + name.replace(/\s/g, ""));
    },
    game: function () {
        this.connect(prompt("Enter server", "ws://127.0.0.1:8080"), prompt("Enter yout name"));
        this.run();
    }
}
