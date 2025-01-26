import sqlite3

salt_len = 16
token_live_time = 60 * 60 * 24  # время, которое будет работать токен (24 часа в секундах)
connection = sqlite3.connect("database.db")
