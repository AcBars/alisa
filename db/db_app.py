import sqlite3


def create_db():
    # создание БД alisa
    # attractive little info system application
    try:
        connection = sqlite3.connect('alisa.db')
        cursor = connection.cursor()
        print("База данных подключена к SQLite")

        with open('alisa.sql', 'r') as sqlite_file:
            sql_script = sqlite_file.read()

        cursor.executescript(sql_script)
        print("Скрипт SQLite успешно выполнен")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (connection):
            connection.close()
            print("Соединение с SQLite закрыто")


# create_db()
# exit()


def read(table):
    try:
        connection = sqlite3.connect('alisa.db', timeout=20)
        cursor = connection.cursor()
        print("Подключен к SQLite")

        # query = 'SELECT * FROM ' + table + ' LIMIT 0, 49999;'
        query = 'SELECT * FROM ' + table + ' LIMIT 0, 49999;'
        cursor.execute(query)
        # cursor.execute(query, (table,))
        selected = cursor.fetchall()
        print(f"{table} : {selected}")
        # print(cursor)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (connection):
            connection.close()
            print("Соединение с SQLite закрыто")


def get_version():
    try:
        connection = sqlite3.connect('alisa.db')
        cursor = connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select sqlite_version();"

        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (connection):
            connection.close()
            print("Соединение с SQLite закрыто")


# get_version()
read('subjects')
exit()
