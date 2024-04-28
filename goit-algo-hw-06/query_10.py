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
select distinct s.name as subject
from subjects s 
join grades g on s.id  = g.subject_id 
join students s2 on g.student_id  = s2.id 
WHERE s2.id = <student_id> AND s.teacher_id = <teacher_id> -- Replace <student and subject_id> with the ID of the specific subject;
"""

print(execute_query(sql))
