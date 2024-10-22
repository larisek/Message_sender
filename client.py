import tkinter as tk
import socket
import pickle
import threading

localhost = input("Server address: ")
port = int(input("Port: "))
def send_message():
    message = message_input.get()
    if message:
        client_socket.send(pickle.dumps(message.encode()))
        message_input.delete(0, tk.END)
        update_chat("You: " + message + '\n')

def receive_messages():
    while True:
        data = client_socket.recv(1024)
        if data:
            message = pickle.loads(data).decode()
            update_chat(message + '\n')

def update_chat(message):
    chat_box.configure(state=tk.NORMAL)
    chat_box.insert(tk.END, message)
    chat_box.configure(state=tk.DISABLED)
    chat_box.see(tk.END)

def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((localhost, port))
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        print("An error occurred while connecting to the server:", str(e))
        return

# Tkinter window
window = tk.Tk()
window.title("Chat Client")

# chatbox
chat_box = tk.Text(window, height=10, width=50)
chat_box.pack(pady=20)
chat_box.configure(state=tk.DISABLED)

# User input
message_input = tk.Entry(window, width=40)
message_input.pack()

# Send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Connect client to server
connect_to_server()

# Run main loop
window.mainloop()

# Close socket
if client_socket:
    client_socket.close()
