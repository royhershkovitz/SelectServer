"""
:Purpose: ping pong TCP select server
:Author: Roy h
:Changes:
28.1.20 change use in select from timeout source to change tracker for small group of sockets
28.1.20 created
"""
import socket
import select
import time
HOST = "0.0.0.0"
PORT = 1337
PING = "ping"
PONG = "pong"
MAX_SELECT_LISTEN_GROUPS = 500
TIMEOUT = 5
SELECT_ITER_TIMEOUT = 0.5


class SelectServer():
    """
    Select server object to manage shared items
    :server: tcp socket object
    :listen_list: the list to track changes
    :conn_timeouts: the last ping time, to disconnect them on timeout!
    """
    def __init__(self, host:str, port:int) -> None:
        """
        :host:
        :port:
        """        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.listen_list = []
        self.conn_timeouts = {}

    def get_timeouts(self, cur_time:int)->list:
        """
        :cur_time:
        :return: list of timed-out connections
        """
        to_remove = []
        for conn, conn_time in self.conn_timeouts.items():
            if cur_time - conn_time > TIMEOUT:
                to_remove.append(conn)
        return to_remove


    def serve(self, listen_group):
        """
        to serve we will wait with select instead of using other blocking methods
        :listen_group: the current group to track changes
        """
        listen_group.append(self.server)
        rlist,_,_ = select.select(listen_group,[],[], SELECT_ITER_TIMEOUT)
        
        cur_time = time.time()
        to_remove = self.get_timeouts(cur_time)
        for conn in rlist:
            if conn == self.server:
                newconn,_ = self.server.accept()
                self.conn_timeouts[newconn] = time.time()
                self.listen_list.append(newconn)
            elif not conn in to_remove:
                data = conn.recv(128)
                data = data.decode().strip()
                if data == PING:
                    conn.send(PONG.encode())
                    self.conn_timeouts[conn] = cur_time
                else:
                    to_remove.append(conn)
                
        for conn in to_remove:
            if conn != self.server:
                conn.close()
                self.listen_list.remove(conn)
                del self.conn_timeouts[conn]

    def start(self):
        """
        The function opens the server on the object interface and port
        """
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(0)
            print("listening at", (self.host, self.port))
            while True:
                try:#MAX_SELECT_LISTEN_GROUPS
                    for group in range(0, len(self.listen_list)+1, MAX_SELECT_LISTEN_GROUPS):
                        self.serve(self.listen_list[group:group+MAX_SELECT_LISTEN_GROUPS])
                except ConnectionResetError:
                    pass
                except KeyboardInterrupt:
                    break
        finally:
            print("Quiting")
            self.server.close()
            self.listen_list.clear()
            self.conn_timeouts.clear()


def main():
    server = SelectServer(HOST, PORT)
    server.start()

if __name__ == "__main__":
    main()
