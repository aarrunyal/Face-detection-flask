import sqlite3
from person import Person

table_create_stmt= "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name varchar(255) not null, age INTEGER not null, email varchar(255) not null, image varchar(255) not null )"

def connection():
    return  sqlite3.connect("face_detection.py")

def create_table():
    conn = connection()
    cur = conn.cursor()
    cur.execute(table_create_stmt)
    conn.commit()
    conn.close()

def insert(user):
    conn = connection();
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?,?,?)", (
        user.id,
        user.name,
        user.age,
        user.email,
        user.image
    ))
    conn.commit()
    conn.close()

def view():
    conn = connection();
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    users = []
    for i in rows:
        user = Person(i[0], i[1], i[2], i[3], "uploads/"+i[4])
        users.append(user)
    conn.close()
    return users

def update(user):
    conn = connection();
    cur = conn.cursor()
    cur.execute("UPDATE users SET available=?, title=? WHERE id=?", (user.name, user.age, user.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = connection();
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = connection();
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
    conn.close()


