from utils import replace_placeholders_in_html


def generate_model_page(model_title, objects):
    if not objects:
        return "<h1>Нет данных для отображения</h1>"

    # Получаем заголовки таблицы (имена столбцов)
    headers = getattr(objects, 'description', None)
    if headers is None:
        return "<h1>Ошибка: не удалось получить описание столбцов</h1>"

    headers_html = "".join(f"<th>{header[0]}</th>" for header in headers)
    # Генерируем строки таблицы
    rows_html = ""
    for row in objects:
        row_html = "".join(f"<td>{value}</td>" for value in row)
        primary_key = row[0]  # Предполагаем, что первое поле - первичный ключ
        actions_html = f"""
        <td>
            <form action="/delete_object" method="post" style="display:inline;">
                <input type="hidden" name="table_name" value="{model_title}">
                <input type="hidden" name="field_value" value="{primary_key}">
                <input type="hidden" name="field_name" value="{headers[0][0]}">
                <button type="submit" class="delete-btn">Удалить</button>
            </form>
            <form action="/admin/{model_title}/create" method="get" style="display:inline;">
                <input type="hidden" name="table_name" value="{model_title}">
                <input type="hidden" name="field_value" value="{primary_key}">
                <input type="hidden" name="field_name" value="{headers[0][0]}">
                <button type="submit" class="edit-btn">Изменить</button>
            </form>
        </td>
        """
        rows_html += f"<tr>{row_html}{actions_html}</tr>"

    # Путь к HTML файлу шаблона
    template_file_path = 'templates/model_page.html'

    # Словарь замен
    replacements_dict = {
        'model_title': model_title,
        'headers_html': headers_html,
        'rows_html': rows_html
    }

    # Заменяем placeholders в HTML файле и получаем обновленное содержимое
    page = replace_placeholders_in_html(template_file_path, replacements_dict)

    return page
