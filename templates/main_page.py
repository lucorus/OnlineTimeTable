import json


def generate_main_page(timetable):
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
