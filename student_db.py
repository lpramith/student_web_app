import sqlite3

def connect():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        course TEXT,
        grade TEXT
    )
    """)
    conn.commit()
    conn.close()
def insert(name, email, course, grade):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, email, course, grade) VALUES (?, ?, ?, ?)",
                (name, email, course, grade))
    conn.commit()
    conn.close()
def view():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return rows
def delete(id):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id=?", (id,))
    conn.commit()
    conn.close()
def update(id, name, email, course, grade):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE student SET name=?, email=?, course=?, grade=? WHERE id=?
    """, (name, email, course, grade, id))
    conn.commit()
    conn.close()
def update(id, name, email, course, grade):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE student SET name=?, email=?, course=?, grade=? WHERE id=?
    """, (name, email, course, grade, id))
    conn.commit()
    conn.close()
