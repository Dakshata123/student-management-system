
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database file location
DB_PATH = os.environ.get("DB_PATH", "students.db")


# Connect to SQLite database
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page: display all students
@app.route("/")
def index():
    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", students=students)


# Add a new student
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    student_id = request.form.get("student_id", "").strip()
    course = request.form.get("course", "").strip()

    if not name or not student_id or not course:
        return "All fields are required", 400

    conn = get_db()

    try:
        conn.execute(
            "INSERT INTO students (name, student_id, course) VALUES (?, ?, ?)",
            (name, student_id, course)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "Student ID already exists", 400

    conn.close()

    return redirect(url_for("index"))


# Update an existing student
@app.route("/update/<int:id>", methods=["POST"])
def update_student(id):
    name = request.form.get("name", "").strip()
    student_id = request.form.get("student_id", "").strip()
    course = request.form.get("course", "").strip()

    if not name or not student_id or not course:
        return "All fields are required", 400

    conn = get_db()

    try:
        result = conn.execute(
            """UPDATE students
               SET name = ?, student_id = ?, course = ?
               WHERE id = ?""",
            (name, student_id, course, id)
        )

        conn.commit()

        if result.rowcount == 0:
            conn.close()
            return "Student not found", 404

    except sqlite3.IntegrityError:
        conn.close()
        return "Student ID already exists", 400

    conn.close()

    return redirect(url_for("index"))


# Delete a student
@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?", (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# Initialize database when application starts
init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

