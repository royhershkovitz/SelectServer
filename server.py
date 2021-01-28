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
    """
    to serve we will wait with select instead of using other blocking methods
    :server: tcp socket object
    """
    rlist,_,_ = select.select([server],[],[])
    conn,_ = server.accept()
    with conn:
        rlist,_,_ = select.select([conn],[],[],TIMEOUT)
        if not rlist:#time out
            return
        data = conn.recv(128)
        data = data.decode().strip()
        if data == PING:
            conn.send(PONG.encode())


def open_server(host, port):
    """
    The function opens the server on these interface and port
    :host:
    :port:
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((host, port))
        server.listen(1)
        print("listening at", (host, port))
        while True:
            try:
                serve(server)
            except ConnectionResetError:
                pass
            except KeyboardInterrupt:
                break
    finally:
        print("Quiting")
        server.close()

def main():
    open_server(HOST, PORT)

if __name__ == "__main__":
    main()