import socket
import pickle
import threading
clients = {}
def handle_client(client_socket):
    while True:
        # příjme zprávu
        data = client_socket.recv(1024)

        if not data:
            break

        # rozkóduje zprávu
        unhashed_data = pickle.loads(data)
        message = unhashed_data.decode()

        # zkontroluje jestli se jedná o změnu jména
        if message.startswith("/name "):
           
            # změní jméno
            name = message[6:]
            clients[client_socket] = name
            print(f"({client_socket.getpeername()[0]}): changed their name to {clients[client_socket]}")
            
            # Uloží /name commandy
            with open("log", "a") as log_file:
                log_file.write(f"({client_socket.getpeername()[0]}): changed their name to {clients[client_socket]}\n")
        else:
            
            # pošle zprávu všem připojeným zařízením
            for c in clients:
                if c != client_socket:
                    c.send(pickle.dumps(f"{clients[client_socket]}: {message}".encode()))
            print(f"({client_socket.getpeername()[0]}): {message}")
           
            # uloží zprávy do log.txt
            with open("log", "a") as log_file:
                log_file.write(f"{clients[client_socket]} ({client_socket.getpeername()[0]}): {message}\n")
   
    # smaže všechny z listu
    del clients[client_socket]
    client_socket.close()

def run_server():
    # Vytvoří soket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # získá IP
    host = socket.gethostbyname(socket.gethostname())

    # dá soketu specifickou adresu
    port = input("Write port you want:")
    while True:
        try:
            int(port)
            break
        except ValueError:
            print("Try it again.")
    server_socket.bind((host, 12345))
    print(f"IP serveru: {host}")

    # Kontroluje připojení
    server_socket.listen(1)

    print("Waiting for a connection...")

    while True:
        # příjme připojení 
        client_socket, client_address = server_socket.accept()

        print(f"Connected to {client_address}")

        # přidá klienta na list
        clients[client_socket] = "Anonymous"

        # odděluje klienty
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    run_server()
