from faker import Faker
import random
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="marv",
    host="localhost",
    port="5432"
)

fake = Faker()
cur = conn.cursor()

groups = [fake.word() for _ in range(3)]
for group in groups:
    cur.execute("INSERT INTO groups (name) VALUES (%s)", [group])

for _ in range(3):
    teacher_name = fake.name()
    cur.execute("INSERT INTO teachers (name) VALUES (%s)", [teacher_name])

for _ in range(5):
    subject = fake.word()
    teacher_id = random.randint(1, 3)  
    cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)", [subject, teacher_id])

for _ in range(30):
    student_name = fake.name()
    group_id = random.randint(1, 3)
    cur.execute("INSERT INTO students (name, group_id) VALUES (%s, %s)", [student_name, group_id])

for student_id in range(1, 31):
    for subject_id in range(1, 6):
        for _ in range(random.randint(1, 20)):
            grade = round(random.uniform(0, 100), 2)  
            date = fake.date_between(start_date='-1y', end_date='today')
            cur.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (%s, %s, %s, %s)",
                        [student_id, subject_id, grade, date])
            
conn.commit()
conn.close()

