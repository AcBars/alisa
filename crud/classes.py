import sqlite3


def insert_classes(level, symbol):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO classes (level, symbol) VALUES(?, ?) ''',
                   (level, symbol))
    conn.commit()

def get_classes():
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM classes''')
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data

def get_class(id_class):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_class, level, symbol 
                        FROM classes 
                        WHERE  = {}'''.format(id_class))
    data = []
    for row in c.fetchall():
        data.append(row)
    return data