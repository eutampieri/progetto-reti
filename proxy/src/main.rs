use std::io::{Read, Write};

fn main() {
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
    let mut buf = vec![];
    loop {
        if let Ok(n) = conn.read(&mut buf) {
            if n > 0 {
                print!("{}", std::str::from_utf8(&buf).unwrap());
            }
        }
    }
}
