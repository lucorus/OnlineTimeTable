import socket
import threading
from contextlib import contextmanager

from midleware import handle_client


@contextmanager
def managed_thread(target, *args):
    thread = threading.Thread(target=target, args=args)
    thread.start()
    try:
        yield
    finally:
        thread.join()


def start_app(domain, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((domain, port))
        server_socket.listen(5)

        print(f"Server started on {domain}:{port}")

        while True:
            try:
                client_socket, address = server_socket.accept()
                with managed_thread(handle_client, client_socket, address):
                    pass
            except socket.error as e:
                print(f"Server socket error: {e}")


if __name__ == "__main__":
    try:
        start_app("localhost", 8083)
    except:
        start_app("localhost", 8084)
