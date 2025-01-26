import socket

from views import *


def route_request(client_socket, request):
    method, url, _ = request.splitlines()[0].split()
    keep_alive = "keep-alive" in request.lower()

    urls = {
        "/": main,
        "/register": register,
        "/users": get_users,
        "/login": login_page,
        "/login_user": login,
        "/create_timetable": create_timetable,

        "/favicon.ico": favicon
    }

    if url in urls:
        urls[url](client_socket=client_socket, request=request, keep_alive=keep_alive)
    else:
        response = make_response(404, "Not Found", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))
        if not keep_alive:
            client_socket.close()


def handle_client(client_socket, address):
    with client_socket:
        try:
            while True:
                request = b""
                while True:
                    chunk = client_socket.recv(2048)
                    if not chunk:
                        break
                    request += chunk

                    if b"\r\n\r\n" in request:
                        break

                if not request:
                    break

                request = request.decode("utf-8")
                route_request(client_socket, request)

        except socket.error as e:
            print(f"Socket error: {e}")
