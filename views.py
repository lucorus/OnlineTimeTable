import datetime

from base_views import page_400
from exceptions import Unauthorized
from utils import (make_response, check_method, encode_string, decode_string, get_cursor, generate_token,
                   login_required, admin_permission_required, Request, generate_uuid)
from database import get_user, get_schools, get_school, delete_object, get_lesson, get_timetable
from templates import login_user_page, register_user_page, main_page


@login_required
def main(request: Request, client_socket):
    cursor = get_cursor()
    school, tracked = request.user["school"], request.user["tracked"]

    if tracked:
        cursor.execute("""
        WITH RankedTimetable AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY timetable.school, timetable.class ORDER BY timetable.date DESC) AS rn
            FROM timetable_object LEFT JOIN timetable ON timetable_object.timetable = timetable.uuid
            LEFT JOIN lesson ON timetable_object.lesson = lesson.uuid
            WHERE timetable.school = ? AND timetable.class = ?
            )
        SELECT *
        FROM RankedTimetable
        WHERE rn = 1;
        """, (school, tracked))
    else:
        cursor.execute("""
        WITH RankedTimetable AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY timetable.school, timetable.class ORDER BY timetable.date DESC) AS rn
            FROM timetable_object LEFT JOIN timetable ON timetable_object.timetable = timetable.uuid
            LEFT JOIN lesson ON timetable_object.lesson = lesson.uuid
            WHERE timetable.school = ?
            )
        SELECT *
        FROM RankedTimetable
        WHERE rn = 1;
        """, (school,))
    timetable = cursor.fetchall()

    page = main_page.generate_main_page(timetable)
    response = make_response(200, page, keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))
    if not request.connection:
        client_socket.close()


@check_method(meth="POST")
def register(request: Request, client_socket):
    try:
        user_info = request.data
        user_info["password"] = encode_string(user_info["password"])

        cursor = get_cursor()
        cursor.execute(
            "INSERT INTO users (username, password, tracked, school) VALUES (?, ?, ?, ?)",
            (user_info["username"], user_info["password"], user_info.get("tracked"), user_info["school_uuid"])
        )
        cursor.connection.commit()

        response = make_response(200, "fiFAIN", keep_alive=request.connection)
        client_socket.sendall(response.encode('utf-8'))
    except Exception as ex:
        print(ex)
        page_400(request, client_socket)


def register_page(request: Request, client_socket):
    response = make_response(200, register_user_page.generate_registration_page(get_schools(get_cursor())), keep_alive=request.connection)
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


def list_schools(request: Request, client_socket):
    try:
        schools = get_schools(get_cursor(), request.data.get("city"))
        response = make_response(200, str(schools), "text/json", keep_alive=request.connection)
        client_socket.sendall(response.encode("utf-8"))
    except Exception as e:
        print(f"list_schools {e}")


@check_method("POST")
@login_required
@admin_permission_required
def create_school(request: Request, client_socket):
    cursor = get_cursor()
    cursor.execute("INSERT INTO school (uuid, title, city) VALUES(?, ?, ?)",
                   (generate_uuid(), request.data["title"], request.data["city"])
                   )
    cursor.connection.commit()
    response = make_response(200, "success!", "text/json", keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
@admin_permission_required
def update_school(request: Request, client_socket):
    cursor = get_cursor()
    cursor.execute(
        "UPDATE school SET title = ?, city = ? WHERE uuid = ?",
        (request.data["title"], request.data["city"], request.data["old_pk"])
    )
    cursor.connection.commit()
    response = make_response(200, "success!", "text/json", keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
def create_user(request: Request, client_socket):
    cursor = get_cursor()
    if not get_school(cursor, request.data["school"]):
        return page_400(request, client_socket)
    cursor.execute("INSERT INTO users (username, password, tracked, school, is_admin) VALUES(?, ?, ?, ?, ?)",
                   (request.data["username"], encode_string(request.data["password"]), request.data.get("tracked"),
                    request.data["school"], request.data.get("is_admin"))
                   )
    cursor.connection.commit()
    response = make_response(200, "success!", "text/json", keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
def update_user(request: Request, client_socket):
    cursor = get_cursor()
    if not get_school(cursor, request.data["school"]):
        return page_400(request, client_socket)
    cursor.execute(
        "UPDATE users SET username = ?, password = ?, tracked = ?, school = ?, is_admin = ? WHERE username = ?",
        (request.data["username"], encode_string(request.data["password"]), request.data.get("tracked"),
         request.data["school"], request.data.get("is_admin"), request.data["old_pk"])
    )
    cursor.connection.commit()
    response = make_response(200, "success!", "text/json", keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
@admin_permission_required
def create_lesson(request: Request, client_socket):
    cursor = get_cursor()
    if not get_school(cursor, request.data["school"]):
        return page_400(request, client_socket)
    cursor.execute("INSERT INTO lesson (uuid, title, school, cabinet) VALUES(?, ?, ?, ?)",
                   (generate_uuid(), request.data["title"], request.data["school"], request.data["cabinet"])
                   )
    cursor.connection.commit()
    response = make_response(201, "success", "text/json", request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
@admin_permission_required
def update_lesson(request: Request, client_socket):
    cursor = get_cursor()
    if not get_school(cursor, request.data["school"]):
        return page_400(request, client_socket)
    cursor.execute(
        "UPDATE lesson SET title = ?, school = ?, cabinet = ? WHERE uuid = ?",
        (request.data["title"], request.data["school"], request.data["cabinet"], request.data["old_pk"])
    )
    cursor.connection.commit()
    response = make_response(200, "success!", "text/json", keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
@admin_permission_required
def create_timetable(request: Request, client_socket):
    cursor = get_cursor()
    if not get_school(cursor, request.data["school"]):
        return page_400(request, client_socket)

    date_str = request.data["date"]
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return page_400(request, client_socket)

    cursor.execute("INSERT INTO timetable (uuid, class, school, date) VALUES(?, ?, ?, ?)",
                   (generate_uuid(), request.data["class"], request.data["school"], formatted_date)
                   )
    cursor.connection.commit()
    response = make_response(201, "success", "text/json", request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
@admin_permission_required
def update_timetable(request: Request, client_socket):
    cursor = get_cursor()
    if not get_school(cursor, request.data["school"]):
        return page_400(request, client_socket)
    cursor.execute(
        "UPDATE timetable SET class = ?, school = ?, date = ? WHERE uuid = ?",
        (request.data["class"], request.data["school"], request.data["date"], request.data["old_pk"])
    )
    cursor.connection.commit()
    response = make_response(200, "success!", "text/json", keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
@admin_permission_required
def create_timetable_object(request: Request, client_socket):
    cursor = get_cursor()
    lesson = get_lesson(cursor, request.data["lesson"])
    if not lesson:
        return page_400(request, client_socket)
    if not get_timetable(cursor, request.data["timetable"]):
        return page_400(request, client_socket)
    cabinet = request.data.get("cabinet") if request.data.get("cabinet") else lesson[3]
    cursor.execute("INSERT INTO timetable_object (uuid, timetable, time, lesson, cabinet) VALUES(?, ?, ?, ?, ?)",
                   (generate_uuid(), request.data["timetable"], request.data["time"], request.data["lesson"],
                    cabinet)
                   )
    cursor.connection.commit()
    response = make_response(201, "success", "text/json", request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")
@login_required
@admin_permission_required
def update_timetable_object(request: Request, client_socket):
    cursor = get_cursor()
    lesson = get_lesson(cursor, request.data["lesson"])
    if not lesson:
        return page_400(request, client_socket)
    if not get_timetable(cursor, request.data["timetable"]):
        return page_400(request, client_socket)
    cabinet = request.data.get("cabinet") if request.data.get("cabinet") else lesson[3]
    cursor.execute(
        "UPDATE timetable_object SET timetable = ?, time = ?, lesson = ?, cabinet = ? WHERE uuid = ?",
        (request.data["timetable"], request.data["time"], request.data["lesson"], cabinet,
         request.data["old_pk"])
    )
    cursor.connection.commit()
    response = make_response(200, "success!", "text/json", keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


@check_method("POST")  # использую post, потому что формочка почему-то отказывается кидать запрос методом delete
@login_required
@admin_permission_required
def delete_object_view(request: Request, client_socket):
    cursor = get_cursor()
    delete_object(cursor=cursor, field_name=request.data["field_name"], field_value=request.data["field_value"],
                  table_name=request.data["table_name"])
    response = make_response(203, "success", "text/json", request.connection)
    client_socket.sendall(response.encode("utf-8"))
