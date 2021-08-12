import socket
import threading
import sys

HEADER = 64
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = None

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            # conn.send("Msg received".encode(FORMAT))

    conn.close()

def start():
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, sock_type, proto, canon_name, sa = res
        try:
            server = socket.socket(af, sock_type, proto)
        except OSError as msg:
            server = None
            continue
        try:
            server.bind(sa)
            server.listen()
            break
        except OSError as msg:
            server.close()
            server = None
            continue
        break
    if server is None:
        print('could not open socket')
        sys.exit(1)
    print(f"[LISTENING] Server is listening on {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting")
start()