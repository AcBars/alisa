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

    
def delete_classes():
    try:
        conn = sqlite3.connect('sqlite_python.db')
        cursor = conn.cursor()
        print("Подключен к SQLite")

        sql_delete_query = """DELETE from classes where id = 6"""
        cursor.execute(sql_delete_query)
        conn.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")

delete_record()