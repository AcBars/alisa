import sqlite3


def insert_subject(subj):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' INSERT INTO subjects(subject) VALUES(?) ''',
        (subj,))
    conn.commit()

