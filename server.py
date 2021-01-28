"""
:Purpose: ping pong TCP select server
:Author: Roy h
:Changes:
28.1.20 created
"""
import socket
import select
HOST = "0.0.0.0"
PORT = 1337
PING = "ping"
PONG = "pong"
TIMEOUT = 5


def serve(server):
    print("listening")
    print(select.select([server],[],[]))
    conn, addr = server.accept()
    with conn:
        print("Connected by", addr)
        print(select.select([conn],[],[],TIMEOUT))
        data = conn.recv(1024)
        if data and data.decode() == PING:
            conn.sendall(PONG.encode())


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen(1)
        while True:
            serve(server)
    finally:
        server.close()

if __name__ == "__main__":
    main()