import datetime
import json
import sqlite3
import uuid

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS school (
        uuid TEXT PRIMARY KEY,
        title TEXT,
        city TEXT
    )
    """
)


"""
tracked - строка, в которой содержится наименование класса расписание, которого отслеживает данный пользователь
если значение не указано, то выводятся расписание для всех классов
password - пароль пользователя, хранящийся в закодированном варианте
"""
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        tracked TEXT NULL,
        school TEXT,
        is_admin BOOL DEFAULT FALSE,
        FOREIGN KEY (school) REFERENCES school(uuid)
    )
    """
)

"""
экземпляр таблицы (расписание для определённого класса в определённой школе на определённую дату)
"""
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS timetable (
        uuid TEXT PRIMARY KEY,
        class TEXT NOT NULL,
        school TEXT,
        date DATE NOT NULL,
        FOREIGN KEY (school) REFERENCES school(uuid)
    )
    """
)


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS lesson (
        uuid TEXT PRIMARY KEY,
        title TEXT,
        school TEXT,
        cabinet TEXT,
        FOREIGN KEY (school) REFERENCES school(uuid)
    )
    """
)


"""
один элемент целого расписания, 

cabinet - в котором проходит урок в данный день (вдруг какое-то изменение), если NULL, 
то будет выставляться значение из lesson 
"""
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS timetable_object (
        uuid TEXT PRIMARY KEY,
        timetable TEXT,
        time TEXT,
        lesson TEXT,
        cabinet TEXT NULL,
        FOREIGN KEY (lesson) REFERENCES lesson(uuid),
        FOREIGN KEY (timetable) REFERENCES timetable(uuid)
    )
    """
)

connection.commit()
connection.close()


def get_user(cursor, username: str) -> str:
    cursor.execute("SELECT * FROM users WHERE username = ?", (username, ))
    user_info = cursor.fetchone()
    return user_info


def get_schools(cursor, city: str = None) -> list:
    if city:
        cursor.execute("SELECT * FROM school WHERE city = ?", (city, ))
    else:
        cursor.execute("SELECT * FROM school")
    return cursor.fetchall()


def get_classes(cursor, school_uuid: str) -> list:
    cursor.execute("SELECT class FROM timetable WHERE school = ?", (school_uuid, ))
    return cursor.fetchall()


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
