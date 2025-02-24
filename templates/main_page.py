from utils import replace_placeholders_in_html


def generate_main_page(schedule_data: list) -> str:
    # Группировка данных по классам и датам
    class_schedule_map = {}
    for entry in schedule_data:
        class_name = entry[6]  # Индекс для класса
        date = entry[8]  # Индекс для даты
        if class_name not in class_schedule_map:
            class_schedule_map[class_name] = {}
        if date not in class_schedule_map[class_name]:
            class_schedule_map[class_name][date] = []
        class_schedule_map[class_name][date].append({
            'time': entry[2],
            'room': entry[4],
            'subject': entry[10]
        })

    # Генерация HTML для каждого класса и даты
    schedule_content = ""
    for class_name, dates in class_schedule_map.items():
        schedule_content += f"""
           <div class="class-schedule">
               <h3>{class_name}</h3>
           """
        for date, schedule in dates.items():
            schedule_content += f"""
               <div class="date-header">{date}</div>
               """
            for entry in schedule:
                schedule_content += f"""
                   <div class="lesson">
                       {entry['time']} {entry['subject']} ({entry['room']})
                   </div>
                   """
        schedule_content += "</div>"

    # Путь к HTML файлу шаблона
    template_file_path = 'templates/main_page.html'

    # Словарь замен
    replacements_dict = {
        'schedule_content': schedule_content
    }

    # Заменяем placeholders в HTML файле и получаем обновленное содержимое
    page = replace_placeholders_in_html(template_file_path, replacements_dict)

    return page
