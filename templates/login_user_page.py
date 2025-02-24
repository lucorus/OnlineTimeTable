from utils import replace_placeholders_in_html


def generate_page(page_title="Login", page_header="Login", form_action="/login_user", submit_button_text="Login"):
    template_file_path = 'templates/login_user_page.html'

    # Словарь замен
    replacements_dict = {
        'page_title': page_title,
        'page_header': page_header,
        'form_action': form_action,
        'submit_button_text': submit_button_text
    }

    # Заменяем placeholders в HTML файле и получаем обновленное содержимое
    page = replace_placeholders_in_html(template_file_path, replacements_dict)

    return page
