import sqlite3

# Connect database
conn = sqlite3.connect("database.db")

# Create cursor
cursor = conn.cursor()

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_number TEXT UNIQUE,
    fullname TEXT,
    password TEXT
)
""")

# Create results table
cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_number TEXT,
    subject TEXT,
    grade TEXT
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database created successfully")
