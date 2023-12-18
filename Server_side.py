import socket
import threading

HOST = '0.0.0.0' #Accepts all IP's
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

clients = {}

def handle_client(client_socket, address):
    client_socket.send("ENTER NAME: ".encode())
    name = client_socket.recv(2048).decode()
    
    print(f"New connection from {name}")

    client_socket.send("Welcome to the chatroom!".encode())

    broadcast(f"{name} has joined the chat!".encode())

    clients[client_socket] = name

    while True:
        try:
            message = client_socket.recv(2048).decode()
            if not message:
                break
            broadcast(f"{name}: {message}".encode())
        except Exception as e:
            print(f"Error: {e}")
            break

    
    broadcast(f"{name} has left the chat.".encode())
    print(f"Lost connection from {name}")
    del clients[client_socket]
    client_socket.close()
    
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(f"Error broadcasting message: {e}")
            del clients[client_socket]

while True:
    client_socket, client_address = server_socket.accept()

    # Create a new thread for the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
