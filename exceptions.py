class Unauthorized(Exception):
    def __init__(self):
        self.message = "Пользователь не авторизирован"

    def __str__(self):
        return self.message


class Forbidden(Exception):
    def __init__(self):
        self.message = "У вас нет доступа к данным ресурсам"

    def __str__(self):
        return self.message


class MethodNotAllowed(Exception):
    def __init__(self, method: str = None):
        if method:
            self.message = f"Данная страница не поддерживает метод {method}"
        else:
            self.message = "Выбранный метод не поддерживается на данной странице"

    def __str__(self):
        return self.message


class InternalServerError(Exception):
    def __init__(self):
        self.message = "Сайт не может обработать ваш запрос >_<"

    def __str__(self):
        return self.message

