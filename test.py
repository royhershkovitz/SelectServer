"""
:Purpose: load test on the ping pong server
:Author: Roy h
:Changes:
28.1.20 created
"""
import socket, time

sockets = [socket.socket() for _ in range(2000)]
count = 0
try:
    for sock in sockets:
        print(f"{count}", end="\r")
        count += 1
        sock.connect(("localhost", 1337))
    print("sleep", end="\r")
    time.sleep(5)
except ConnectionRefusedError:
    print(count)
