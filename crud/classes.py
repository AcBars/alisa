import sqlite3


def insert_classes(level, symbol):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO classes (level, symbol) VALUES(?, ?) ''',
                   (level, symbol))
    conn.commit()
