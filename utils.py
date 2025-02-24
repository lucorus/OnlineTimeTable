import base64
import datetime
import os
import sqlite3
import uuid

import config
from database import get_user
from exceptions import Unauthorized, InternalServerError, Forbidden, MethodNotAllowed


def func(s: str, split_symbol: str = ";", del_key: bool = True) -> dict:
    """
    Данная функция должна разделять строки cookie и data на словарь, в котором будет храниться содержание данных строк
    split_symbol - указывает после какого символа нужно разделять строку (нужно, потому что data разделяется знаком "&",
    а cookie ";")
    del_key - нужно ли удалять ключ (data просто находится в последней строке request, а cookie на 7 строке после слова
    Cookie)
    """
    try:
        if del_key:
            # пропускаем первое слово в строке, которое обозначает чем является строка (cookie и т.п.)
            s = s[s.find(" "):]
        s = s.split(split_symbol)
        ans = {}
        for i in s:
            ind = i.find("=")
            try:
                key, value = i[:ind], i[ind+1:]
            except IndexError:
                # если значение для данного ключа нет, то просто устанавливаем для него None
                key, value = i[0], None

            if value:
                # если в конце и начале ключа иди значения есть " или ', то убираем их
                if (value[0] == value[-1] and value[-1] == '"') or (value[0] == value[-1] and value[-1] == "'"):
                    value = value[1:-1]
            if key:
                if (key[0] == key[-1] and key[-1] == '"') or (key[0] == key[-1] and key[-1] == "'"):
                    key = key[1:-1]
                if key[0] == " ":
                    key = key[1:]

            ans[key] = value
        return ans
    except IndexError:
        # если отправляются запросы без cookie/data, то будет возникать эта ошибка
        return {}
    except Exception as ex:
        print(f"func error: {ex}")
        return {}


def parse_request(request: list) -> dict:
    """
    Делаем из request'а словарь
    """
    request_dict = {}

    for line in request:
        # Разделяем строку на ключ и значение
        if ':' in line:
            key, value = line.split(':', 1)
            request_dict[key.strip()] = value.strip()
        else:
            # Если в строке нет ':', сохраняем её как есть
            request_dict[line.strip()] = ''

    return request_dict


class Request:

    def __init__(self, request):
        request = request.splitlines()
        data_str = request[-1]  # строчка, в которой содержится data
        method, url, _ = request[0].split()
        request = parse_request(request[1:])
        self.connection = "keep-alive" if request.get("Connection") == "keep-alive" else False
        if "?" in url:
            data_str = url[url.index("?")+1:]  # если data передана в url запроса, то отмечаем её, как data
            url = url[:url.index("?")]
        self.method = method
        self.url = url.split("/")[1:]
        self.data = func(data_str, "&", False)
        self.cookie = func(request.get("Cookie"))
        self._request_user_username = None  # используется вместо показателя авторизирован ли пользователь или нет
        self._request_user = {}

    @property
    def user(self) -> dict:
        """
        получаем данные текущего пользователя
        """
        if self._request_user == {}:
            user = get_user(get_cursor(), self.is_login)
            user = {
                "username": user[0],
                "password": user[1],
                "tracked": user[2],
                "school": user[3],
                "is_admin": user[4]
            }
            self._request_user = user
        return self._request_user

    @property
    def is_login(self):
        """
        получаем имя залогиненного пользователя
        """
        if self._request_user_username == None:
            try:
                username = token_is_valid(self.cookie["Authorization"])
                self._request_user_username = username
            except Exception as ex:
                print(f"error in is_login: {ex}")
                self._request_user_username = False
        return self._request_user_username


def generate_uuid() -> str:
    return str(uuid.uuid4())


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
    def decorator(function):
        def wrapper(*args, **kwargs):
            if kwargs["request"].method == meth:
                return function(*args, **kwargs)
            else:
                raise MethodNotAllowed(kwargs["request"].method)
        return wrapper
    return decorator


def login_required(function):
    def wrapper(*args, **kwargs):
        try:
            request = kwargs["request"]
            if request.is_login:
                return function(*args, **kwargs)
            else:
                raise Unauthorized
        except Unauthorized or TypeError:  # TypeError может возникать, если не переданы cookie
            raise Unauthorized
        except Exception as ex:
            print(f"login_required error: {ex}")
            raise InternalServerError
    return wrapper


def admin_permission_required(function):
    def wrapper(*args, **kwargs):
        if kwargs["request"].user["is_admin"]:
            return function(*args, **kwargs)
        else:
            raise Forbidden
    return wrapper


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


def replace_placeholders_in_html(file_path, replacements) -> str:
    """
    Открывает HTML файл и заменяет {% placeholder %} на значения из словаря replacements. (подобно jinja)

    :param file_path: Путь к HTML файлу.
    :param replacements: Словарь, где ключи - это placeholders, а значения - то, на что нужно заменить.
    :return: Строка с измененным содержимым HTML файла.
    """
    try:
        # Открываем файл и читаем его содержимое
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Заменяем все placeholders на значения из словаря
        for key, value in replacements.items():
            placeholder = f"{{% {key} %}}"
            content = content.replace(placeholder, value)

        return content
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
