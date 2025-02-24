from utils import replace_placeholders_in_html


def generate_registration_page(schools: list) -> str:
    school_options = ''.join(
        f'<option value="{uuid}" data-city="{city}">{title} <span style="font-size: 0.8em; color: #888;">({city})</span></option>'
        for uuid, title, city in schools
    )

    # Путь к HTML файлу шаблона
    template_file_path = 'templates/register_user_page.html'

    # Словарь замен
    replacements_dict = {
        'school_options': school_options
    }

    # Заменяем placeholders в HTML файле и получаем обновленное содержимое
    page = replace_placeholders_in_html(template_file_path, replacements_dict)

    return page
