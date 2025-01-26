import datetime
import json

from utils import (make_response, check_method, encode_string, decode_string, get_cursor, generate_token,
                   login_required, request_user_username, admin_permission_required, get_data)
from database import get_user, create_timetable_instance


@login_required
def main(client_socket, request, keep_alive):
    username = request_user_username(request)
    cursor = get_cursor()
    user = get_user(cursor, username)
    school, tracked = user[3], user[2]

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

    main_page = generate_main_page(timetable)
    response = make_response(200, main_page, keep_alive=keep_alive)
    client_socket.sendall(response.encode('utf-8'))
    if not keep_alive:
        client_socket.close()


def generate_main_page(timetable):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Timetable</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h1>Timetable</h1>
        <table>
            <tr>
                <th>UUID</th>
                <th>Class</th>
                <th>School</th>
                <th>Date</th>
                <th>Lessons</th>
            </tr>
            {timetable_rows}
        </table>
    </body>
    </html>
    """

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


def favicon(client_socket, request, keep_alive):
    response = make_response(404, "Not Found", keep_alive=keep_alive)
    client_socket.sendall(response.encode('utf-8'))
    if not keep_alive:
        client_socket.close()


@check_method(meth="POST")
@admin_permission_required
def create_timetable(client_socket, request, keep_alive):
    try:
        body = request.splitlines()[-1]
        timetable_info = json.loads(body)
        timetable_info["lessons"] = json.loads(timetable_info["lessons"])

        create_timetable_instance(get_cursor(), **timetable_info)

        response = make_response(200, "Timetable created successfully", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))

    except Exception as ex:
        print(ex)
        response = make_response(400, "Bad request", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))


@check_method(meth="POST")
def register(client_socket, request, keep_alive):
    try:
        # получаем данные в удобном формате
        user_info = get_data(request)

        user_info["password"] = encode_string(user_info["password"])

        cursor = get_cursor()
        cursor.execute(
            "INSERT INTO users (username, password, tracked, school) VALUES (?, ?, ?, ?)",
            (user_info["username"], user_info["password"], user_info["tracked"], user_info["school"])
        )
        cursor.connection.commit()

        response = make_response(200, "fiFAIN", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))

        if not keep_alive:
            client_socket.close()
    except Exception as ex:
        print(ex)
        response = make_response(400, "Bad request", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))


def get_users(client_socket, request, keep_alive):
    try:
        cursor = get_cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        response = make_response(200, f"\n {users}", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))
    except Exception as ex:
        print(ex)
        response = make_response(400, "Bad request", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))


@check_method("POST")
def login(client_socket, request, keep_alive):
    try:
        # получаем данные в удобном формате
        user_info = get_data(request)

        cursor = get_cursor()
        user = get_user(cursor, user_info["username"])

        password = decode_string(user[1])
        if password == user_info["password"]:
            # пользователь подтвердил, что он владелец аккаунта
            token = generate_token(user_info["username"])
            headers = {
                "Set-Cookie": f"Authorization={token}; Path=/; HttpOnly",
                "Location": "/"
            }
            response = make_response(200, "GOOD", keep_alive=keep_alive, headers=headers)
            client_socket.sendall(response.encode('utf-8'))
        else:
            response = make_response(401, "Unauthorized", keep_alive=keep_alive)
            client_socket.sendall(response.encode('utf-8'))

    except Exception as ex:
        print(ex)
        response = make_response(400, "Bad request", keep_alive=keep_alive)
        client_socket.sendall(response.encode('utf-8'))


def login_page(client_socket, request, keep_alive):
    log_page = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form action="/login_user" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""
    response = make_response(200, log_page, keep_alive=keep_alive)
    client_socket.sendall(response.encode('utf-8'))
