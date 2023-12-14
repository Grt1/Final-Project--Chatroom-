import socket
import select
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: python script.py <IP_address> <port_number>")
    sys.exit(1)

IP_address = '127.0.0.1'
Port = '8080'

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    conn.send(b"Welcome to this chatroom!")  # Convert the string to bytes

    while True:
        try:
            message = conn.recv(2048)
            if message:
                print("<" + addr[0] + "> " + message.decode())  # Decode received bytes to string

                message_to_send = "<" + addr[0] + "> " + message.decode()
                broadcast(message_to_send, conn)

            else:
                remove(conn)

        except Exception as e:
            print(e)
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())  # Encode the message to bytes before sending
            except Exception as e:
                print(e)
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()

    list_of_clients.append(conn)

    print(addr[0] + " connected")

    start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
