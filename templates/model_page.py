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
                <input type="hidden" name="field_name" value="{headers_html[4:headers_html.index('</th>')]}">
                <button type="submit" class="delete-btn">Удалить</button>
            </form>
            <form action="/edit_object" method="post" style="display:inline;">
                <input type="hidden" name="table_name" value="{model_title}">
                <input type="hidden" name="primary_key" value="{primary_key}">
                <button type="submit" class="edit-btn">Изменить</button>
            </form>
        </td>
        """
        rows_html += f"<tr>{row_html}{actions_html}</tr>"

    page = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Администраторская панель - {model_title}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f0f2f5;
                margin: 0;
                padding: 0;
                color: #333;
            }}
            .container {{
                width: 80%;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }}
            h1 {{
                text-align: center;
                color: #007bff;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #007bff;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            tr:hover {{
                background-color: #ddd;
            }}
            .delete-btn, .edit-btn {{
                padding: 5px 10px;
                margin: 2px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .delete-btn {{
                background-color: #dc3545;
                color: white;
            }}
            .delete-btn:hover {{
                background-color: #c82333;
            }}
            .edit-btn {{
                background-color: #ffc107;
                color: white;
            }}
            .edit-btn:hover {{
                background-color: #e0a800;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Администраторская панель - {model_title}</h1>
            <table>
                <thead>
                    <tr>
                        {headers_html}
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return page
