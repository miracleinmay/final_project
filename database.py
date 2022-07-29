import sqlite3


# создаём базу данных для сохранения результатов
db = sqlite3.connect("2048.sqlite")

cur = db.cursor()

# создаём таблицу с результатами
cur.execute("""
CREATE TABLE IF NOT EXISTS RECORDS (
name text, 
score integer
)""")

# получаем 3 лучших результата
def get_best():
    cur.execute("""
    SELECT name gamer, max(score) score from RECORDS
    GROUP by name
    ORDER by score DESC
    limit 3
    """)
    return cur.fetchall()

# запись результата после геймовера
def insert_result(name, score):
    cur.execute("INSERT INTO RECORDS VALUES (?, ?)", (name, score))
    db.commit()

print(get_best())

