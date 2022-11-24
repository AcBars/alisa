import sqlite3


def insert(level, symbol):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO classes (level, symbol) VALUES(?, ?) ''',
                   (level, symbol))
    conn.commit()


def get_all():
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM classes''')
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data


def get(id_class):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_class, level, symbol 
                        FROM classes 
                        WHERE  id_class = {}'''.format(id_class))
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data


def update(id_class, level, symbol):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE classes 
                    SET level = ?, symbol = ? 
                    WHERE  id_class = ?''',
                   (level, symbol, id_class))
    conn.commit()
