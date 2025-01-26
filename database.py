import datetime
import json
import sqlite3
import uuid

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

"""
tracked - строка, в которой содержится наименование класса расписание, которого отслеживает данный пользователь
если значение не указано, то выводятся расписание для всех классов
school - номер школы для которой нужно выводить расписание данному пользователю
"""
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        tracked TEXT NULL,
        school INT NOT NULL,
        is_admin BOOL DEFAULT FALSE
    )
    """
)

"""
экземпляр таблицы (расписание для определённого класса в определённой школе на определённую дату)
lessons - поле, которое хранит список уроков в формате json в виде
[ 
    {"subject": "Math(401)", "time": "9:00"-"9:40"},
    ...
]
"""
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS timetable (
        uuid TEXT PRIMARY KEY,
        class TEXT NOT NULL,
        school INT NOT NULL,
        date TEXT NOT NULL,
        lessons TEXT NOT NULL 
    )
    """
)

connection.commit()
connection.close()


def get_user(cursor, username: str) -> str:
    cursor.execute("SELECT * FROM users WHERE username = ?", (username, ))
    user_info = cursor.fetchone()
    return user_info


def create_timetable_instance(cursor, class_name, school, lessons):
    table_uuid = str(uuid.uuid4())
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    lessons_json = json.dumps(lessons)

    cursor.execute(
        """
        INSERT INTO timetable (uuid, class, school, date, lessons)
        VALUES (?, ?, ?, ?, ?)
        """,
        (table_uuid, class_name, school, date, lessons_json)
    )
    cursor.connection.commit()
