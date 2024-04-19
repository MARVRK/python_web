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


sql = """
  SELECT
    t.name AS teacher_name,
    ROUND(AVG(g.grade)::numeric, 2) AS average_grade
FROM teachers AS t
JOIN subjects AS s ON t.id = s.teacher_id
JOIN grades AS g ON s.id = g.subject_id
GROUP BY t.id, t.name;

"""

print(execute_query(sql))
