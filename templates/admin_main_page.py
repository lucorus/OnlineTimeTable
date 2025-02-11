def generate_page(models):
    tabs_html = ""
    for model in models:
        tab_html = f'<li><a href="/admin/{model}" class="tab">{model.capitalize()}</a></li>'
        tabs_html += tab_html

    page = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Администраторская панель</title>
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
            .tabs {{
                list-style-type: none;
                padding: 0;
            }}
            .tab {{
                background-color: #007bff;
                color: white;
                padding: 15px 30px;
                margin: 10px 0;
                border-radius: 5px;
                text-decoration: none;
                display: block;
                transition: background-color 0.3s;
            }}
            .tab:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Администраторская панель</h1>
            <ul class="tabs">
                {tabs_html}
            </ul>
        </div>
    </body>
    </html>
    """
    return page
