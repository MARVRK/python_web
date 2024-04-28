from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from structure import Student, Group, Teacher, Subject, Grade, DATABASE_URL
from random import randint
from datetime import datetime, timedelta

fake = Faker()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

groups = [Group(name=fake.random_elements(["Group A", "Group B", "Group C"])) for _ in range(3)]
session.add_all(groups)
session.commit()

teachers = [Teacher(name=fake.random_elements()) for _ in range (3)]
session.add_all(teachers)
session.commit()

subjects = [Subject(name=fake.random_elements(["Maths", "Physics", "Computer Sience", "Soldering", "Algorythms"]),teacher_id = randint(1,3)) for _ in range(5)] 
session.add_all(subjects)
session.commit()

students = []
for _ in range(30):
    student = Student(name=fake.name())
    session.add(student)
    session.commit()
    students.append(student)

for student in students:
    for subject in subjects:
        score = randint(1,100)
        date= datetime.now() - timedelta(days = randint(0, 365))
        grade = Grade(student_id = student.id, subject_id = subject.id, score = score, date = date)
        session.add(grade)
session.commit()