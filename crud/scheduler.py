import sqlite3


def insert_schedule(id_week, time_start, id_class, id_subject):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO schedule 
                    (id_week, time_start, id_class, id_subject) 
                    VALUES(?, ?, ?, ?) ''',
                   (id_week, time_start, id_class, id_subject))
    conn.commit()


def get_schedules():
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_week, time_start, id_class, id_subject 
                    FROM schedule''')
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data


def get_schedule(id_schedule):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_week, time_start, id_class, id_subject 
                        FROM schedule 
                        WHERE  id_schedule = {}'''.format(id_schedule))
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data
