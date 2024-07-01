import sqlite3

from settings import DATABASE_FILE


def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT)''')
    db.commit()
    db.close()

    return


def get_db():
    db = sqlite3.connect(DATABASE_FILE)
    return db


def insert_file(filename):
    filename = str(filename)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM uploads WHERE filename = ?', (filename, ))
    file_cursor = cursor.fetchone()
    if file_cursor is None:
        cursor.execute("insert into uploads (filename) values (?)", [filename, ])
        file_id = cursor.lastrowid
        conn.commit()
        file_exist = False
    else:
        file_id = file_cursor[0]
        file_exist = True

    cursor.close()
    conn.close()

    return file_id, file_exist


def select_file(file_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT filename FROM uploads WHERE id = ?', (file_id,))
    result = cursor.fetchone()

    if result is None:
        filename = False
    else:
        filename = result[0]
    conn.close()

    return filename


if __name__ == '__main__':
    insert_file(filename="place_your_bets.wav")
