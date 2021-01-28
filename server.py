"""
:Purpose: ping pong TCP select server
:Author: Roy h
:Changes:
28.1.20 created
"""
import socket
import select
import time
HOST = "0.0.0.0"
PORT = 1337
PING = "ping"
PONG = "pong"
TIMEOUT = 5


def get_timeouts(conn_timeouts:dict, cur_time:int)->list:
    """
    :conn_timeouts: the last ping to disconnect them!
    :cur_time:
    :return: timeout connections
    """
    to_remove = []
    for conn, conn_time in conn_timeouts.items():
        if conn_time - cur_time > TIMEOUT:
            to_remove.append(conn)
    return to_remove


def serve(server, listen_list:list, conn_timeouts:dict):
    """
    to serve we will wait with select instead of using other blocking methods
    :server: tcp socket object
    :listen_list: the list to track changes
    :conn_timeouts: the last ping to disconnect them!
    """    
    rlist,_,_ = select.select(listen_list,[],[], TIMEOUT)
    
    cur_time = time.time()
    to_remove = get_timeouts(conn_timeouts, cur_time)
    if rlist == []:#timeout all connections
        to_remove = listen_list
    else:
        for conn in rlist:
            if conn == server:
                conn,_ = server.accept()
                conn_timeouts[conn] = time.time()
                listen_list.append(conn)
            elif not conn in to_remove:
                data = conn.recv(128)
                data = data.decode().strip()
                if data == PING:
                    conn.send(PONG.encode())
                    conn_timeouts[conn] = cur_time
                else:
                    to_remove.append(conn)
            
    for conn in to_remove:
        if conn != server:
            conn.close()
            listen_list.remove(conn)
            del conn_timeouts[conn]


def open_server(host:str, port:int):
    """
    The function opens the server on these interface and port
    :host:
    :port:
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((host, port))
        server.listen()
        print("listening at", (host, port))
        listen_list = [server]
        conn_timeouts = {}
        while True:
            try:
                serve(server, listen_list, conn_timeouts)
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