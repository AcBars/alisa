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

        query = 'SELECT * FROM ' + table + ' LIMIT 0, 49999;'
        cursor.execute(query)
        # cursor.execute(query, (table,))
        selected = cursor.fetchall()
        print(f"{table} : {selected}")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (connection):
            connection.close()
            print("Соединение с SQLite закрыто")


def update(table):
    try:
        connect = sqlite3.connect('alisa.db')
        cursor = connect.cursor()
        print("Подключен к SQLite")

        update = """Update table set  field1 = ? where id = ?"""
        cursor.execute(update, 2, 1)
        connect.commit()
        print("Запись успешно обновлена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connect:
            connect.close()
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


def delete(id):
    try:
        connect = sqlite3.connect('sqlite_python.db')
        cursor = connect.cursor()
        print("Подключен к SQLite")

        deletion = """DELETE from sqlitedb_developers where id = ?"""
        cursor.execute(deletion, (id,))
        connect.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connect:
            connect.close()
            print("Соединение с SQLite закрыто")


def check_table_fields(table, fields_dict):
    try:
        connection = sqlite3.connect('alisa.db', timeout=20)
        cursor = connection.cursor()
        query = 'pragma  table_info({});'.format(table)
        cursor.execute(query)
        selected = cursor.fetchall()

        for key in fields_dict:
            for fields in selected:
                founded = False
                if key in fields:
                    founded = True
                    break
            if not founded:
                print('что-то не так с наименованиями полей')
                cursor.close()
                return founded
        # print(f"{table} : {selected}")
        cursor.close()
        return founded
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (connection):
            connection.close()
            # print("Соединение с SQLite закрыто")


def crud(action, table, fields_dict):
    if not check_table_fields(table, fields_dict):
        return False
    try:
        connection = sqlite3.connect('alisa.db', timeout=20)
        cursor = connection.cursor()
        query = create_query(action, table, fields_dict)
        # print(query)
        cursor.execute(query)
        # selected = cursor.fetchall()
        connection.commit()
        connection.close()
        return fields_dict
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    # finally:
    #     if (connection):
    #         connection.close()
    #         #print("Соединение с SQLite закрыто")


def create_query(action, table, fields_as_dict):
    if action.lower() == 'insert':
        query = 'INSERT INTO {} ('.format(table)
        for key in fields_as_dict:
            query += '{}, '.format(key)
        query = query.rstrip(', ')
        query += ') VALUES ('
        for key, val in fields_as_dict.items():
            if type(val) == str:
                query += "'{}',".format(val)
            else:
                query += "{},".format(val)
        query = query.rstrip(',')
        query += ')'
    if action.lower() == 'update':
        print('update')
    if action.lower() == 'delete':
        print('delete')
    return query


print(crud('insert', 'classes', {'level': 5, 'symbol': 'Г'}))
read('classes')

exit()
