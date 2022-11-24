import sqlite3


def add_students(classes, pupils, grade, items):
    try:
        connection = sqlite3.connect('alisa.db')
        # Соединиться с базой данных с помощью sqlite3.connect()

        cursor = connection.cursor()
        # Подготовить запрос создания таблицы

        print("База данных создана и успешно подключена к SQLite")

        data = [classes, pupils, grade, items]
        cursor.execute(f"INSERT INTO students VALUES(?, ?, ?, ?);", data)
        # Выполнить запрос с помощью cursor.execute(query)
        connection.commit()
        cursor.close()  # Закрыть соединение с базой и объектом cursor

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (connection):
            connection.close()
            print("Соединение с SQLite закрыто")
