import socket
import threading

HOST = '127.0.0.1'
PORT = 5555
name = ""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

clients = []

def handle_client(client_socket, address):
    print(f"New connection from {address}")

    client_socket.send("Welcome to the chatroom!".encode())
    name = input("Enter a name: ")

    broadcast(f"{address} has joined the chat!".encode())

    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message)
        except Exception as e:
            print(f"Error: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()
    broadcast(f"{address} has left the chat.".encode())

def broadcast(message):
    for client in clients:
        try:
            client.send(name,":", message)
        except Exception as e:
            print(f"Error broadcasting message: {e}")
            clients.remove(client)

while True:
    client_socket, client_address = server_socket.accept()

    # Create a new thread for the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
