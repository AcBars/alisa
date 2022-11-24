import sqlite3


def insert(first_name, second_name, id_class):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''  INSERT INTO students (first_name, second_name, id_class) 
                        VALUES(?, ?, ?) ''',
                        (first_name, second_name, id_class))
    conn.commit()

def get_all():
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_student, first_name, second_name, id_class  
                    FROM students''')
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data

def get(id_student):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_student, first_name, second_name, id_class 
                        FROM students 
                        WHERE  id_student = {}'''.format(id_student))
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data

def update(id_student, first_name, second_name, id_class):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE students SET first_name = ?,
                        second_name = ?, 
                        id_class = ?
                        WHERE  id_student = ?''',
                   (first_name, second_name, id_class,id_student))
    conn.commit()