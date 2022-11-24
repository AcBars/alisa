import sqlite3


def insert_student(id_student, first_name, second_name, id_class):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO students (id_student, first_name, second_name, id_class) VALUES(?, ?, ?, ?, ?) ''',
               (id_student, first_name, second_name, id_class))
    conn.commit()

