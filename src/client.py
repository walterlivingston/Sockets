import threading
import socket
import sys

HEADER = 64
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'q'

client = None

def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def receive(conn):
    while True:
        print(conn.recv(2048).decode(FORMAT))

def start():
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, sock_type, proto, canon_name, sa = res
        try:
            client = socket.socket(af, sock_type, proto)
        except OSError as msg:
            client = None
            continue
        try:
            client.connect(sa)
        except OSError as msg:
            client.close()
            client = None
            continue
        break
    if client is None:
        print("Could not open socket.")
        sys.exit(1)
    with client:
        while True:
            receive_thread = threading.Thread(target=receive, args=(client,))
            receive_thread.start()

            send_thread = threading.Thread(target=send, args=(client, input()))
            send_thread.start()

start()