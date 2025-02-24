from datetime import datetime

from utils import replace_placeholders_in_html


def generate_model_create_page(model_title, columns, instance):
    fields_html = ""
    hidden_input = ""
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

        # Получаем значение поля из экземпляра, если оно существует
        field_value = ""
        if instance:
            field_value = instance[columns.index(column_name)]

        if "TEXT" in column_type:
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><input type="text" id="{column_name}" name="{column_name}" value="{field_value}" {"required" if column_required else ""}>'
        elif "INT" in column_type:
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><input type="number" id="{column_name}" name="{column_name}" value="{field_value}" {"required" if column_required else ""}>'
        elif "BOOL" in column_type:
            selected_true = "selected" if field_value == "TRUE" else ""
            selected_false = "selected" if field_value == "FALSE" else ""
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><select id="{column_name}" name="{column_name}" {"required" if column_required else ""}><option value="TRUE" {selected_true}>TRUE</option><option value="FALSE" {selected_false}>FALSE</option></select>'
        elif "DATE" in column_type:
            # Преобразование формата даты для отображения
            date_value = ""
            if field_value:
                try:
                    date_obj = datetime.strptime(field_value, "%Y-%m-%d")
                    date_value = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    date_value = ""
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><input type="date" id="{column_name}" name="{column_name}" value="{date_value}" {"required" if column_required else ""}>'
        else:
            field_html = f'<label for="{column_name}">{column_name.capitalize()}</label><input type="text" id="{column_name}" name="{column_name}" value="{field_value}" {"required" if column_required else ""}>'
        fields_html += field_html

    if instance:
        hidden_input = f'<input type="hidden" name="old_pk" value="{instance[0]}">'

    # Путь к HTML файлу шаблона
    template_file_path = 'templates/model_create_page.html'

    # Словарь замен
    replacements_dict = {
        'model_title': model_title,
        'page_title': f'Создать новую запись - {model_title}' if not instance else f'Изменить запись {instance[0]}',
        'form_action': f'/update_{model_title}' if instance else f'/create_{model_title}',
        'hidden_input': hidden_input,
        'fields_html': fields_html
    }

    # Заменяем placeholders в HTML файле и получаем обновленное содержимое
    page = replace_placeholders_in_html(template_file_path, replacements_dict)

    return page
