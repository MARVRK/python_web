import psycopg2


def execute_query(sql: str) -> list:
    with psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="marv",
        host="localhost",
        port="5432") as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """SELECT
    s.name AS student_name,
    ROUND(AVG(g.grade)::numeric, 2) AS average_grade,
    sub.name AS subject_name
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sub ON g.subject_id = sub.id
WHERE g.subject_id = <subject_id>  -- Replace <subject_id> with the ID of the specific subject
GROUP BY s.id, s.name, sub.id, sub.name
ORDER BY average_grade DESC
LIMIT 1;
"""

print(execute_query(sql))



