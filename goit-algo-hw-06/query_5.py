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
SELECT DISTINCT name AS course_name
FROM subjects
WHERE teacher_id = <teacher_id>; -- Replace <teacher_id> with the ID of the specific subject
"""

print(execute_query(sql))
