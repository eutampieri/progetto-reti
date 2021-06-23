use std::{
    borrow::BorrowMut,
    io::{Read, Write},
};
use websocket::OwnedMessage;

fn main() {
    let server = websocket::server::sync::Server::bind("[::]:8080").expect("Faild to start proxy");
    for request in server.filter_map(Result::ok) {
        // Spawn a new thread for each connection.
        std::thread::spawn(|| {
            let mut conn = std::net::TcpStream::connect((
                std::env::args().nth(1).expect("Provide an address"),
                std::env::args()
                    .nth(2)
                    .expect("Provide a port number")
                    .parse::<u16>()
                    .expect("Provide a valid port number"),
            ))
            .expect("Cannot connect to the server");
            conn.write_all(b"api").expect("Cannot write to server");
            conn.set_read_timeout(None).unwrap();
            conn.set_nonblocking(false).unwrap();
            let mut recv_conn = conn.try_clone().unwrap();

            let client = request.accept().unwrap();
            let (mut receiver, mut sender) = client.split().unwrap();
            let mut sender_arc = std::sync::Arc::new(sender);
            let mut recv_sender_arc = sender_arc.clone();

            std::thread::spawn(move || {
                let mut buf = [0u8; 1000];

                loop {
                    if let Ok(n) = recv_conn.read(&mut buf) {
                        if n > 0 {
                            let recieved = Vec::from(&buf[0..n]);
                            let msg = OwnedMessage::Binary(recieved);
                            recv_sender_arc.borrow_mut().send_message(&msg).unwrap();
                        }
                    }
                }
            });

            for message in receiver.incoming_messages().filter(|x| x.is_ok()) {
                let message = dbg!(message).unwrap();

                match message {
                    OwnedMessage::Close(_) => {
                        let message = OwnedMessage::Close(None);
                        sender_arc.send_message(&message).unwrap();
                        println!("Client {} disconnected", 0);
                        return;
                    }
                    OwnedMessage::Ping(ping) => {
                        let message = OwnedMessage::Pong(ping);
                        sender_arc.send_message(&message).unwrap();
                    }
                    OwnedMessage::Text(txt) => conn
                        .write_all(txt.as_bytes())
                        .expect("Couldn't write to raw TCP"),
                    _ => sender_arc.send_message(&message).unwrap(),
                }
            }
        });
    }
}
