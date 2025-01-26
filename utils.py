import base64
import datetime
import os
import sqlite3

import config
from database import get_user


def make_response(status_code: int, content: str, content_type: str = "text/html", keep_alive: bool = False,
                  headers: dict = None):
    headers = headers or {}
    headers["Content-Type"] = content_type
    headers["Content-Length"] = str(len(content))
    headers["Connection"] = "keep-alive" if keep_alive else "close"

    status_line = f"HTTP/1.1 {status_code} {status_code}\r\n"
    headers_line = "\r\n".join(f"{key}: {value}" for key, value in headers.items())
    response = f"{status_line}{headers_line}\r\n\r\n{content}"

    return response


def check_method(meth: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            method, url, _ = kwargs["request"].splitlines()[0].split()
            if method == meth:
                return func(*args, **kwargs)
            else:
                response = make_response(405, "Method Not Allowed", keep_alive=kwargs["keep_alive"])
                kwargs["client_socket"].sendall(response.encode('utf-8'))
                return response
        return wrapper
    return decorator


def login_required(func):
    def wrapper(*args, **kwargs):
        try:
            username = request_user_username(kwargs["request"])
            if username:
                return func(*args, **kwargs)
            else:
                response = make_response(401, "Unauthorized", keep_alive=kwargs["keep_alive"])
                kwargs["client_socket"].sendall(response.encode('utf-8'))
        except Exception as ex:
            print(ex)
            response = make_response(500, "Internal Server Error", keep_alive=kwargs["keep_alive"])
            kwargs["client_socket"].sendall(response.encode('utf-8'))
    return wrapper


def admin_permission_required(func):
    def wrapper(*args, **kwargs):
        username = request_user_username(kwargs["request"])
        user = get_user(get_cursor(), username)
        if user[-1]:
            return func(*args, **kwargs)
        else:
            response = make_response(403, "Forbidden", keep_alive=kwargs["keep_alive"])
            kwargs["client_socket"].sendall(response.encode('utf-8'))
    return wrapper


def request_user_username(request):
    """
    Получает имя пользователя, который отправляет запрос
    """
    try:
        # получаем строку токена из куков
        cookie = request.splitlines()[7]
        cookie = cookie.split()
        for item in cookie:
            if item[:13] == "Authorization":
                token = item[14:]
                break

        username = token_is_valid(token)
        return username
    except Exception as ex:
        print(ex)


def get_cursor():
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        return cursor


def generate_token(username: str) -> str:
    """
    Создаёт токен, хранящий в себе информацию о дате его создания и пользователе, которому он принадлежит;
    используется, как jwt токен
    """
    time_now = datetime.datetime.now()
    time_str = time_now.strftime("%d/%m/%Y %H:%M:%S")
    token = time_str + username
    token = encode_string(token)
    return token


def token_is_valid(token: str) -> str:
    """
    Получает токен, проверяет не просрочен ли он. если всё нормально, то возвращает ник пользователя
    """
    s = decode_string(token)
    time_str = s[:19]  # длина, которую занимает время в указанном формате
    username = s[19:]

    token_time = datetime.datetime.strptime(time_str, "%d/%m/%Y %H:%M:%S")
    current_time = datetime.datetime.now()

    if (current_time - token_time).total_seconds() <= config.token_live_time:
        return username


def generate_salt():
    return os.urandom(config.salt_len)


def encode_string(s: str) -> str:
    input_bytes = s.encode()
    salt = generate_salt()
    input_bytes_with_salt = salt + input_bytes
    encoded_bytes = base64.b64encode(input_bytes_with_salt)
    encoded_string = encoded_bytes.decode()
    return encoded_string


def decode_string(s: str) -> str:
    encoded_bytes = s.encode()
    decoded_bytes_with_salt = base64.b64decode(encoded_bytes)
    decoded_bytes = decoded_bytes_with_salt[config.salt_len:]
    decoded_string = decoded_bytes.decode()
    return decoded_string


def get_data(request):
    """
    Получает данные из data, пакуя их в словарь по их ключу в data
    """
    # получаем данные в удобном формате
    data = request.splitlines()[-1]  # data находится на последней строчке request
    data = data.split("&")

    info = {}

    for item in data:
        key, value = item.split("=")
        info[key] = value

    return info
