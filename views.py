import datetime
import json

from base_views import page_400
from exceptions import Unauthorized
from utils import (make_response, check_method, encode_string, decode_string, get_cursor, generate_token,
                   login_required, admin_permission_required, Request)
from database import get_user, create_timetable_instance
from templates import main_page, login_user_page, register_user_page


@login_required
def main(request: Request, client_socket):
    cursor = get_cursor()
    school, tracked = request.user["school"], request.user["tracked"]
    now = datetime.datetime.now()

    date = now.strftime("%d-%m-%Y")

    if tracked:
        cursor.execute("""
            SELECT * FROM timetable WHERE school = ? AND class = ?
        """, (school, tracked, ))
    else:
        cursor.execute("""
            SELECT * FROM timetable WHERE school = ?
        """, (school, ))
    timetable = cursor.fetchall()

    page = generate_main_page(timetable)
    response = make_response(200, page, keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))
    if not request.connection:
        client_socket.close()


def generate_main_page(timetable):
    html_template = main_page.page

    # Генерация строк таблицы для расписания
    timetable_rows = ""
    for entry in timetable:
        uuid, class_name, school, date, lessons_json = entry
        lessons = json.loads(lessons_json)
        lessons_html = "<br>".join([f"{lesson['subject']} ({lesson['time']})" for lesson in lessons])
        timetable_rows += f"""
        <tr>
            <td>{uuid}</td>
            <td>{class_name}</td>
            <td>{school}</td>
            <td>{date}</td>
            <td>{lessons_html}</td>
        </tr>
        """

    return html_template.replace("{timetable_rows}", timetable_rows)


@check_method(meth="POST")
@login_required
@admin_permission_required
def create_timetable(client_socket, request: Request, data: str):
    try:
        timetable_info = json.loads(data)
        timetable_info["lessons"] = json.loads(timetable_info["lessons"])

        create_timetable_instance(get_cursor(), **timetable_info)

        response = make_response(200, "Timetable created successfully", keep_alive=request.connection)
        client_socket.sendall(response.encode('utf-8'))

    except Exception as ex:
        print(ex)
        response = make_response(400, "Bad request")
        client_socket.sendall(response.encode('utf-8'))


@check_method(meth="POST")
def register(request: Request, client_socket):
    try:
        user_info = request.data
        user_info["password"] = encode_string(user_info["password"])

        cursor = get_cursor()
        cursor.execute(
            "INSERT INTO users (username, password, tracked, school) VALUES (?, ?, ?, ?)",
            (user_info["username"], user_info["password"], user_info["tracked"], user_info["school"])
        )
        cursor.connection.commit()

        response = make_response(200, "fiFAIN", keep_alive=request.connection)
        client_socket.sendall(response.encode('utf-8'))
    except Exception as ex:
        print(ex)
        page_400(request, client_socket)


def register_page(request: Request, client_socket):
    response = make_response(200, register_user_page.page, keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))


def get_users(request: Request, client_socket):
    try:
        cursor = get_cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        response = make_response(200, f"\n {users}", keep_alive=request.connection)
        client_socket.sendall(response.encode('utf-8'))
    except Exception as ex:
        print(ex)
        page_400(request, client_socket)


@check_method("POST")
def login(request: Request, client_socket):
    try:
        user_info = request.data
        user = get_user(get_cursor(), user_info["username"])
        password = decode_string(user[1])
        if password == user_info["password"]:
            # пользователь подтвердил, что он владелец аккаунта
            token = generate_token(user_info["username"])
            headers = {
                "Set-Cookie": f"Authorization={token}; Path=/; HttpOnly",
                "Location": "/"
            }
            response = make_response(200, "GOOD", keep_alive=request.connection, headers=headers)
            client_socket.sendall(response.encode('utf-8'))
        else:
            raise Unauthorized

    except Exception as ex:
        print(ex)
        page_400(request, client_socket)


def login_page(request: Request, client_socket):
    response = make_response(200, login_user_page.page, keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))
