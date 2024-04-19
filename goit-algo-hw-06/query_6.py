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


sql = """SELECT s.name as students
from students s 
where group_id = <selct_group_id> -- Replace <group_id> with the ID of the specific subject
"""

print(execute_query(sql))
