import socket
import threading
import sys

HEADER = 64
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'q'

server = None
clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            for c in clients: c.send(f"[{addr}] {msg}".encode(FORMAT))

    clients.remove(conn)
    conn.close()

def server_send():
    msg = input()
    print(f"[SERVER] {msg}".encode(FORMAT))
    for c in clients: c.send(f"[SERVER] {msg}".encode(FORMAT))

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
            server.listen(1)
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
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

        send_thread = threading.Thread(target=server_send, args=())
        send_thread.start()
        thread_count = threading.activeCount()
        thread_count -= 2 if threading.activeCount() >= 3 else 1
        print(f"[ACTIVE CONNECTIONS] {thread_count}")

print("[STARTING] server is starting")
start()