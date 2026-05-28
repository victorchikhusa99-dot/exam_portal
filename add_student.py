import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Add student
cursor.execute("""
INSERT INTO students(exam_number, fullname, password)
VALUES(?,?,?)
""", (
    "MSCE001",
    "Victor Chikhusa",
    "1234"
))

# Add results
cursor.execute("""
INSERT INTO results(exam_number, subject, grade)
VALUES(?,?,?)
""", (
    "MSCE001",
    "Mathematics",
    "1"
))

cursor.execute("""
INSERT INTO results(exam_number, subject, grade)
VALUES(?,?,?)
""", (
    "MSCE001",
    "English",
    "2"
))

conn.commit()
conn.close()

print("Student added successfully")
