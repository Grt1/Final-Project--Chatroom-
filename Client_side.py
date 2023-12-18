import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

IP = '127.0.0.1'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"Connecting to {IP}:{PORT}")
client_socket.connect((IP, PORT))

# Tkinter GUI
root = tk.Tk()
root.title("Chatroom")

# Create scrolled text area for messages
messages_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
messages_area.pack(padx=10, pady=10)

# Entry widget for user input
entry_field = Entry(root, width=30)
entry_field.pack(padx=10, pady=10)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            messages_area.insert(tk.END, message + '\n')
            messages_area.see(tk.END)  # Scroll to the bottom
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Create a thread for receiving messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def send_message(event=None):
    message = entry_field.get()
    if message:
        client_socket.send(message.encode())
        entry_field.delete(0, tk.END)  # Clear the entry field

# Button to send messages
send_button = Button(root, text="Send", command=send_message)
send_button.pack(pady=10)

root.bind('<Return>', send_message)

root.mainloop()
