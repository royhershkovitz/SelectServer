import socket, time

sockets = [socket.socket() for _ in range(2000)]
count = 0
try:
    for sock in sockets:
        count += 1
        sock.connect(("localhost", 1337))
    time.sleep(5)
except ConnectionRefusedError:
    print(count)
