def generate_model_create_page(model_title, columns):
    fields_html = ""
    for column in columns:
        column_name = column

        column_type = "TEXT"
        match column:
            case "is_admin":
                column_type = "BOOL"
            case "date":
                column_type = "DATE"

        column_required = True
        if column_name in ["tracked", "cabinet"]:
            column_required = False

        if "TEXT" in column_type or "DATE" in column_type:
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><input type="text" id="{column_name}" name="{column_name}" {"required" if column_required else ""}>'
        elif "INT" in column_type:
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><input type="number" id="{column_name}" name="{column_name}" {"required" if column_required else ""}>'
        elif "BOOL" in column_type:
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><select id="{column_name}" name="{column_name}" {"required" if column_required else ""}><option value="TRUE">TRUE</option><option value="FALSE">FALSE</option></select>'
        else:
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><input type="text" id="{column_name}" name="{column_name}" {"required" if column_required else ""}>'
        fields_html += field_html

    page = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Создать новую запись - {model_title}</title>
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
            form {{
                display: flex;
                flex-direction: column;
            }}
            label {{
                margin-bottom: 5px;
                font-weight: bold;
            }}
            input, select {{
                margin-bottom: 15px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            button {{
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Создать новую запись - {model_title}</h1>
            <form id="createForm" action="/create_{model_title}" method="post">
                {fields_html}
                <button type="submit">Создать</button>
            </form>
        </div>
        <script>
            document.getElementById('createForm').addEventListener('submit', function(event) {{
                event.preventDefault();
                const formData = new FormData(event.target);
                const data = {{}};
                formData.forEach((value, key) => {{
                    data[key] = value;
                }});
                fetch(event.target.action, {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify(data)
                }}).then(response => response.text())
                  .then(result => {{
                      alert('Запись успешно создана!');
                      window.location.reload();
                  }})
                  .catch(error => {{
                      console.error('Ошибка:', error);
                      alert('Произошла ошибка при создании записи.');
                  }});
            }});
        </script>
    </body>
    </html>
    """
    return page
