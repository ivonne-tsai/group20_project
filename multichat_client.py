#client
import socket
import threading
import sys


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode()
            print(msg)
        except OSError:
            break


def client_send():
    while True:
        try:
            msg1 = input()
            client_socket.send(msg1.encode())
            if msg1 == 'quit':
                break
        except OSError:
            sys.exit(1)
    client_socket.close()


if __name__ == '__main__':
    HOST = input('Enter host IP: ')
    PORT = input('Enter port: ')
    PORT = int(PORT)
    BUFSIZE = 1024

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()
