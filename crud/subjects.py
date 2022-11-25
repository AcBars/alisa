import sqlite3


def insert(subj):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' INSERT INTO subjects(subject) VALUES(?) ''',
        (subj,))
    conn.commit()


def get_all():
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_subject, subject
                    FROM subjects''')
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data


def get(id_subject):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_subject, subject 
                        FROM subjects 
                        WHERE  id_subject = {}'''.format(id_subject))
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data


def update(id_subject, subj):
    conn = sqlite3.connect('alisa.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE subjects SET subject = ?
                        WHERE  id_subject = ?''', (subj, format(id_subject)))
    conn.commit()
