from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Record Management System</title>
    <style>
        body{
            font-family: Arial;
            margin:40px;
            background:#f4f4f4;
        }
        h1{
            color:#333;
        }
        form{
            background:white;
            padding:20px;
            border-radius:10px;
            margin-bottom:20px;
        }
        input{
            padding:10px;
            margin:5px;
            width:200px;
        }
        button{
            padding:10px 15px;
            background:#007bff;
            color:white;
            border:none;
            border-radius:5px;
        }
        table{
            width:100%;
            background:white;
            border-collapse:collapse;
        }
        th,td{
            border:1px solid #ddd;
            padding:10px;
            text-align:center;
        }
        th{
            background:#007bff;
            color:white;
        }
        a{
            color:red;
            text-decoration:none;
        }
    </style>
</head>
<body>

<h1>Student Record Management System</h1>

<form method="POST" action="/add">
    <input type="text" name="name" placeholder="Student Name" required>
    <input type="text" name="roll_no" placeholder="Roll Number" required>
    <input type="text" name="department" placeholder="Department" required>
    <input type="number" name="semester" placeholder="Semester" required>
    <button type="submit">Add Student</button>
</form>

<table>
<tr>
    <th>ID</th>
    <th>Name</th>
    <th>Roll No</th>
    <th>Department</th>
    <th>Semester</th>
    <th>Action</th>
</tr>

{% for student in students %}
<tr>
    <td>{{ student[0] }}</td>
    <td>{{ student[1] }}</td>
    <td>{{ student[2] }}</td>
    <td>{{ student[3] }}</td>
    <td>{{ student[4] }}</td>
    <td>
        <a href="/delete/{{ student[0] }}">Delete</a>
    </td>
</tr>
{% endfor %}
</table>

</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template_string(HTML, students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll_no = request.form['roll_no']
    department = request.form['department']
    semester = request.form['semester']

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (name, roll_no, department, semester) VALUES (?, ?, ?, ?)",
            (name, roll_no, department, semester)
        )
        conn.commit()
    except:
        pass

    conn.close()

    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
