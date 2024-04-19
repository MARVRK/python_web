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
SELECT s.name AS student_name, ROUND(AVG(g.grade)::numeric, 2) AS average_grade
from students as s
join grades as g on s.id  = g.student_id
group by s.id ,s."name" 
ORDER BY average_grade DESC
limit 5;
"""

print(execute_query(sql))

