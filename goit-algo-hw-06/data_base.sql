CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    group_id INTEGER REFERENCES groups(id)
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    teacher_id INTEGER REFERENCES teachers(id)
);

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    subject_id INTEGER REFERENCES subjects(id),
    grade FLOAT,
    date DATE
);
