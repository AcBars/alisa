import sqlite3


def insert_subject(subj):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' INSERT INTO subjects(subject) VALUES(?) ''',
        (subj,))
    conn.commit()

def get_subjects():
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_subject, subject
                    FROM subjects''')
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data

def get_subject(id_subject):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_subject, subject 
                        FROM subjects 
                        WHERE  id_subject = {}'''.format(id_subject))
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data
