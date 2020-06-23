import socket
import select; import sys
from _thread import start_new_thread
from threading import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Uses script, IP adress and port number")


ip_address = '127.0.0.1'

port = int(4455)

server.bind((ip_address, port))
#Max of 10 connections
server.listen(10)
clients = []

def clientsthread(conn, addr):
    conn.send(b'Welcome to the round timer')
    while True:
        try:
            message = conn.recv(2048)
            if message:
                print("<" + addr[0] + ">" + message)

                message_to_send = "<" + addr[0] + ">" + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for client in clients:
        if clients != connection:
            try:
                client.send(message)
            except:
                client.close()

                remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)
while True:

    conn, addr = server.accept()

    clients.append(conn)

    print( addr[0] + " connected")

    start_new_thread(clientsthread, (conn, addr))

conn.close()
server.close()