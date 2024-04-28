from sqlalchemy import func, desc, select, and_
from structure import Grade, Teacher, Student, Group, Subject
from seed import session

def request_1():
    '''
SELECT s.fullname, round(avg(g.grade), 2) AS avg_grade
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 5;
    '''
    result = (
    session.query(
        Student.name.label('student_name'),
        func.round(func.avg(Grade.score), 2).label('average_grade'),
        Student.id
    )
    .join(Grade, Student.id == Grade.student_id)
    .group_by(Student.id, Student.name, Student.id)
    .order_by(func.avg(Grade.score).desc())
    .limit(5)
    .all()
)
    for row in result:
        print(f"Student Name: {row.student_name}, Average Grade: {row.average_grade}, Student ID: {row.id}")

def request_2():
    '''
    SELECT
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
    '''
    subject_id = 11  # <--- Select subject id by putting the number

    result = (
    session.query(
        Student.name.label('student_name'),
        func.round(func.avg(Grade.score), 2).label('average_grade'),
        Subject.name.label("subject_name")
    )
    .join(Grade, Student.id == Grade.student_id)
    .join(Subject, Grade.subject_id == Subject.id )
    .filter(Grade.subject_id == subject_id)
    .group_by(Student.id, Student.name, Subject.id, Subject.name)
    .order_by(func.avg(Grade.score).desc())
    .limit(1)
    .all()
    )
    for row in result:
        print(f"Student Name: {row.student_name}, Average Grade: {row.average_grade}, Subject_name: {row.subject_name}")
    
def request_3():
    '''
    SELECT
    g2.name AS group_name,
    ROUND(AVG(g.grade)::numeric, 2) AS average_grade
FROM grades AS g
JOIN students AS s ON g.student_id = s.id
JOIN groups AS g2 ON s.group_id = g2.id
WHERE g.subject_id = 1  -- Replace <subject_id> with the ID of the specific subject
GROUP BY g2.id, g2.name
ORDER BY group_name;
    '''
    subject_id = 2  # <--- Select subject id by putting the number

    result = (
    session.query(
        Group.name.label('group_name'),
        func.round(func.avg(Grade.score), 2).label('average_grade'),
    )
    .join(Student, Group.id == Student.group_id)
    .join(Grade, Student.id == Grade.student_id )
    .filter(Grade.subject_id == subject_id)
    .group_by(Group.name, Group.id)
    .order_by(Group.name)
    .all()
    )
    for row in result:
        print(f"Group Name: {row.group_name}, Average Grade: {row.average_grade}")
    


def request_4():
    '''
    SELECT ROUND(AVG(grade)::numeric, 2) AS average_grade FROM grades;
    '''
    result = (
    session.query(
        func.round(func.avg(Grade.score), 2).label('average_grade'),
    )
    .order_by(func.avg(Grade.score).desc())
    .all()
    )
    for row in result:
        print(f"Average Grade: {row.average_grade}")


def request_5():
    """
SELECT DISTINCT name AS course_name
FROM subjects
WHERE teacher_id = <teacher_id>; -- Replace <teacher_id> with the ID of the specific subject
    """

    teacher_id = 3  # <--- Select teacher id by putting the number

    result = (
    session.query(Subject.name.label("Course_name"))
    .filter(Subject.teacher_id == teacher_id)
    .all()
    )
    for row in result:
        print(f"Subject: {row.Course_name}")


def request_6():
    '''SELECT s.name as students
    from students s 
    where group_id = <selct_group_id> -- Replace <group_id> with the ID of the specific subject
    '''
    group_id = 1  # <--- Select group id by putting the number

    result = (
    session.query(Student.name.label("Students"))
    .filter(Student.group_id == group_id)
    .all()
    )
    for row in result:
        print(f"Students: {row.Students}")
    
def request_7():
    """select s.name as subject, g.grade as grades
from grades g
join subjects as s on s.id  = g.student_id
join students s2 ON g.student_id = s2.id 
where s2.group_id  = <selct_group_id> -- Replace <group_id> with the ID of the specific subject
group by s.id , g.grade;
"""
    group_id = 1  # <--- Select group id by putting the number

    result = (session.query(Subject.name.label('subject'), Grade.score.label('grades'))
    .join(Grade, Subject.id == Grade.subject_id)
    .join(Student, Grade.student_id == Student.id)
    .filter(Student.group_id == group_id)
    .group_by(Subject.id, Grade.score)
    .all()
    )
    for row in result:
        print(f"Subject: {row.subject}, Grade: {row.grades}")

def request_8():
    """
  SELECT
    t.name AS teacher_name,
    ROUND(AVG(g.grade)::numeric, 2) AS average_grade
FROM teachers AS t
JOIN subjects AS s ON t.id = s.teacher_id
JOIN grades AS g ON s.id = g.subject_id
GROUP BY t.id, t.name;

"""
    result = (session.query(Teacher.name.label('teacher_name'),
    func.round(func.avg(Grade.score), 2).label('average_grade'))
    .join(Subject, Teacher.id == Subject.teacher_id)
    .join(Grade, Subject.id == Grade.subject_id)
    .group_by(Teacher.id, Teacher.name)
    .all()
    )
    for row in result:
        print(f"Teacher_name: {row.teacher_name}, Ave. Grades: {row.average_grade}")



def request_9():
    """select distinct  s.name as subjects
from subjects s
join grades g on s.id  = g.subject_id 
join students s2 on g.student_id  = s2.id 
where s2.id  = 27-- Replace <student_id> with the ID of the specific subject;
"""
    student_id = 1  # <--- Select student id by putting the number

    result = (session.query(Subject.name.label('subjects'))
    .join(Grade, Subject.id == Grade.subject_id)
    .join(Student, Grade.student_id == Student.id)
    .filter(Grade.subject_id == student_id)
    .distinct()
    .all()
    )
    for row in result:
        print(f"Subjects: {row.subjects}")

def request_10():
    """
select distinct s.name as subject
from subjects s 
join grades g on s.id  = g.subject_id 
join students s2 on g.student_id  = s2.id 
WHERE s2.id = <student_id> AND s.teacher_id = <teacher_id> -- Replace <student and subject_id> with the ID of the specific subject;
"""
    student_id = 2  # <--- Select student id by putting the number
    teacher_id = 2  # <--- Select teacher id by putting the number
    
    result = (session.query(Subject.name.label('subject'))
    .join(Grade, Subject.id == Grade.subject_id)
    .join(Student, Grade.student_id == Student.id)
    .filter(and_(Student.id == student_id, Subject.teacher_id == teacher_id))
    .distinct()
    .all()
    )
    for row in result:
        print(f"Subjects: {row.subject}")


if __name__ == "__main__" :
    request_10() # <--- Select request by changing the number         