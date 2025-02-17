import sqlite3

# Opret forbindelse til SQLite databasen (filen 'school.db') Opretter filen, hvis den ikke eksitere i mappen
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Opret 'Students' tabellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    major TEXT
)
""")

# Opret 'Courses' tabellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    instructor TEXT
)
""")

# Opret 'Enrollments' tabellen, som forbinder Students og Courses
cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)
""")

# Indsæt mindst 5 records i 'Students' tabellen
students = [
    (1, "Alice", "Computer Science"),
    (2, "Bob", "Mathematics"),
    (3, "Charlie", "Physics"),
    (4, "Diana", "Biology"),
    (5, "Eve", "Chemistry")
]
cursor.executemany("INSERT INTO Students (student_id, name, major) VALUES (?, ?, ?)", students)

# Indsæt mindst 5 records i 'Courses' tabellen
courses = [
    (1, "Database Systems", "Dr. Smith"),
    (2, "Calculus", "Dr. Johnson"),
    (3, "Quantum Mechanics", "Dr. Lee"),
    (4, "Genetics", "Dr. White"),
    (5, "Organic Chemistry", "Dr. Brown")
]
cursor.executemany("INSERT INTO Courses (course_id, course_name, instructor) VALUES (?, ?, ?)", courses)

# Indsæt nogle records i 'Enrollments' tabellen, som forbinder studerende og kurser
enrollments = [
    (1, 1, 1),  # Alice er tilmeldt Database Systems
    (2, 1, 2),  # Alice er tilmeldt Calculus
    (3, 2, 2),  # Bob er tilmeldt Calculus
    (4, 3, 3),  # Charlie er tilmeldt Quantum Mechanics
    (5, 4, 4),  # Diana er tilmeldt Genetics
    (6, 5, 5),  # Eve er tilmeldt Organic Chemistry
    (7, 2, 1),  # Bob er også tilmeldt Database Systems
    (8, 3, 1)   # Charlie er også tilmeldt Database Systems
]
cursor.executemany("INSERT INTO Enrollments (enrollment_id, student_id, course_id) VALUES (?, ?, ?)", enrollments)

# Gem ændringerne
conn.commit()

# Forespørgsel: Vælg alle kurser, som en specifik studerende (f.eks. student_id = 1) er tilmeldt
student_id = 1
cursor.execute("""
SELECT Courses.course_id, Courses.course_name, Courses.instructor
FROM Courses
JOIN Enrollments ON Courses.course_id = Enrollments.course_id
WHERE Enrollments.student_id = ?
""", (student_id,))
student_courses = cursor.fetchall()
print(f"Student med ID {student_id} er tilmeldt følgende kurser:")
for course in student_courses:
    print(course)


# Forespørgsel: Vælg alle studerende, der er tilmeldt et specifikt kursus (f.eks. course_id = 1)
course_id = 1
cursor.execute("""
SELECT Students.student_id, Students.name, Students.major
FROM Students
JOIN Enrollments ON Students.student_id = Enrollments.student_id
WHERE Enrollments.course_id = ?
""", (course_id,))
course_students = cursor.fetchall()
print(f"\nFølgende studerende er tilmeldt kursus med ID {course_id}:")
for student in course_students:
    print(student)

# Luk forbindelsen til databasen
conn.close()
