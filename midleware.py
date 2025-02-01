import socket

from views import *
from utils import Request


def route_request(client_socket, request):
    req = Request(request)
    keep_alive = "keep-alive" in request.lower()

    urls = {
        "/": main,
        "/register": register_page,
        "/register_user": register,
        "/users": get_users,
        "/login": login_page,
        "/login_user": login,
        "/create_timetable": create_timetable,

        "/favicon.ico": favicon  # адрес, по которому обращается браузер для получения иконки
    }

    if req.url in urls:
        if req.url == "/create_timetable":
            # для этой функции нужно отдельно посылать данные, потому что она работает с датой формата json
            urls[req.url](client_socket=client_socket, request=req, data=request.splitlines()[-1])
        else:
            urls[req.url](request=req, client_socket=client_socket)
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
