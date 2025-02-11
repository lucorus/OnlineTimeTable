import sqlite3

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


def get_school(cursor, uuid: str) -> tuple:
    cursor.execute("SELECT 1 FROM school WHERE uuid = ?", (uuid, ))
    return cursor.fetchone()


def get_lesson(cursor, lesson_uuid):
    cursor.execute("SELECT 1 FROM lesson WHERE uuid = ?", (lesson_uuid, ))
    return cursor.fetchone() is not None


def get_timetable(cursor, timetable_uuid):
    cursor.execute("SELECT 1 FROM timetable WHERE uuid = ?", (timetable_uuid, ))
    return cursor.fetchone() is not None


def delete_object(cursor, field_name, field_value, table_name) -> None:
    """
    Удаляет объект из таблицы table_name, у которого столбец с названием field_name равен field_value
    """
    cursor.execute(f"DELETE FROM {table_name} WHERE {field_name} = ?", (field_value, ))
    cursor.connection.commit()
