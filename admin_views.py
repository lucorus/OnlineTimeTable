from base_views import page_404
from utils import (make_response, get_cursor, Request)
from templates import admin_main_page, model_page, model_create_page


# Список моделей, которые будут отображаться на странице админа
models = ["school", "users", "timetable", "lesson", "timetable_object"]


# @login_required
# @admin_permission_required
def admin_route_request(request: Request, client_socket):
    urls = {
        "": admin_main,

        "create": create_page,

        "school": model_view,
        "users": model_view,
        "timetable": model_view,
        "lesson": model_view,
        "timetable_object": model_view,
    }
    if request.url[-1] in urls:
        urls[request.url[-1]](request, client_socket)
    else:
        page_404(request, client_socket)


def admin_main(request: Request, client_socket):
    page = admin_main_page.generate_page(models)
    response = make_response(200, page, keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


def model_view(request: Request, client_socket):
    model_title = request.url[-1]
    if model_title not in models:
        page_404(request, client_socket)
        return
    cursor = get_cursor()
    objects = cursor.execute(f"SELECT * FROM {model_title}")
    page = model_page.generate_model_page(model_title, objects)
    response = make_response(200, page, keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))


def create_page(request: Request, client_socket):
    model_title = request.url[1]
    if model_title not in models:
        page_404(request, client_socket)
        return

    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM {model_title} LIMIT 0")
    columns = cursor.description
    columns = [i[0] for i in columns]

    page = model_create_page.generate_model_create_page(model_title, columns)
    response = make_response(200, page, keep_alive=request.connection)
    client_socket.sendall(response.encode("utf-8"))
