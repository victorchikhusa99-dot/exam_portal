
from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)

app.secret_key = "admin123"
@app.route("/", methods=["GET", "POST"])
def login():
    if "admin" not in session:
        return redirect("/admin-login")

    if request.method == "POST":

        exam_number = request.form["exam_number"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE exam_number=? AND password=?
        """, (exam_number, password))

        student = cursor.fetchone()

        if student:

            cursor.execute("""
            SELECT id, subject, grade
            FROM results
            WHERE exam_number=?
            """, (exam_number,))

            results = cursor.fetchall()

            conn.close()

            return render_template(
                "results.html",
                results=results,
                exam_number=exam_number
            )

        else:
            conn.close()
            return "Wrong Details"

    return render_template("login.html")
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if "admin" not in session:
        return redirect("/admin-login")
    if request.method == "POST":

        exam_number = request.form["exam_number"]
        subject = request.form["subject"]
        grade = request.form["grade"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM results
        WHERE exam_number=? AND subject=?
        """, (exam_number, subject))

        existing = cursor.fetchone()

        if existing:

            conn.close()
            return "Subject Already Uploaded"

        cursor.execute("""
        INSERT INTO results(exam_number, subject, grade)
        VALUES(?,?,?)
        """, (exam_number, subject, grade))

        conn.commit()
        conn.close()

        return "Result Uploaded Successfully"


    return render_template("admin.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if "admin" not in session:
        return redirect("/admin-login")

    if request.method == "POST":

        exam_number = request.form["exam_number"]
        fullname = request.form["fullname"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO students(exam_number, fullname, password)
        VALUES(?,?,?)
        """, (exam_number, fullname, password))

        conn.commit()
        conn.close()

        return "Student Registered Successfully"

    return render_template("register.html")

@app.route("/delete/<int:id>")
def delete(id):

    if "admin" not in session:
        return redirect("/admin-login")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM results
    WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return "Result Deleted Successfully"

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "admin" not in session:
        return redirect("/admin-login")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        subject = request.form["subject"]
        grade = request.form["grade"]

        cursor.execute("""
        UPDATE results
        SET subject=?, grade=?
        WHERE id=?
        """, (subject, grade, id))

        conn.commit()
        conn.close()

        return "Result Updated Successfully"

    cursor.execute("""
    SELECT * FROM results
    WHERE id=?
    """, (id,))

    result = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        result=result
    )

@app.route("/manage")
def manage():

    if "admin" not in session:
        return redirect("/admin-login")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

   
  
    cursor.execute("""
    SELECT
    results.id,
    students.fullname,
    results.exam_number,
    results.subject,
    results.grade

    FROM results

    JOIN students
     ON results.exam_number = students.exam_number
       """)
    

    results = cursor.fetchall()

    conn.close()

    return render_template(
        "manage.html",
        results=results
    )

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":

            session["admin"] = True

            return redirect("/manage")

        else:
            return "Wrong Admin Details"

    return render_template("admin_login.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/admin-login")
app.run(host="0.0.0.0", port=5000)
