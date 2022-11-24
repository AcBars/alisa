import sqlite3


def insert_student(first_name, second_name, id_class):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''  INSERT INTO students (first_name, second_name, id_class) 
                        VALUES(?, ?, ?) ''',
                        (first_name, second_name, id_class))
    conn.commit()

