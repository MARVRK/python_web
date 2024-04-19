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


sql = """select s.name as subject, g.grade as grades
from grades g
join subjects as s on s.id  = g.student_id
join students s2 ON g.student_id = s2.id 
where s2.group_id  = <selct_group_id> -- Replace <group_id> with the ID of the specific subject
group by s.id , g.grade;
"""

print(execute_query(sql))
