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
    g2.name AS group_name,
    ROUND(AVG(g.grade)::numeric, 2) AS average_grade
FROM grades AS g
JOIN students AS s ON g.student_id = s.id
JOIN groups AS g2 ON s.group_id = g2.id
WHERE g.subject_id = 1  -- Replace <subject_id> with the ID of the specific subject
GROUP BY g2.id, g2.name
ORDER BY group_name;

"""

print(execute_query(sql))
