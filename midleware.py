import socket

from views import *
from exceptions import Unauthorized, Forbidden, MethodNotAllowed
from utils import Request
from base_views import page_403, page_404, page_405, page_500, favicon


def route_request(client_socket, request):
    req = Request(request)

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
        try:
            if req.url == "/create_timetable":
                # для этой функции нужно отдельно посылать данные, потому что она работает с датой формата json
                urls[req.url](client_socket=client_socket, request=req, data=request.splitlines()[-1])
            else:
                urls[req.url](request=req, client_socket=client_socket)
        except Unauthorized:
            # если пользователь не авторизован, а страница этого требует, то перебрасываем его на страницу login'а
            urls["/login"](request=req, client_socket=client_socket)
        except Forbidden:
            page_403(req, client_socket)
        except MethodNotAllowed:
            page_405(req, client_socket)
        except:
            page_500(req, client_socket)
    else:
        page_404(req, client_socket)


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
