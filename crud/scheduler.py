import sqlite3


def insert_schedule(id, day_of_week, time_start, id_class, id_subject):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' INSERT INTO schedule (id, day_of_week, time_start, id_class, id_subject) VALUES(?, ?, ?, ?, ?) ''',
        (id, day_of_week, time_start, id_class, id_subject))
    conn.commit()
