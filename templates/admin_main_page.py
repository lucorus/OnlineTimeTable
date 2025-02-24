from utils import replace_placeholders_in_html


def generate_page(models):
    tabs_html = ""
    for model in models:
        tab_html = f'<li><a href="/admin/{model}" class="tab">{model.capitalize()}</a></li>'
        tabs_html += tab_html

    # Путь к HTML файлу
    html_file_path = 'templates/admin_main_page.html'

    # Словарь замен
    replacements_dict = {
        'tabs_html': tabs_html
    }

    # Заменяем placeholders в HTML файле и получаем обновленное содержимое
    page = replace_placeholders_in_html(html_file_path, replacements_dict)

    return page
