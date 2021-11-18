from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import mysql.connector

#hi

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="student_database"
)

mycursor = db.cursor(buffered=True)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    if session.get("username"):
        return redirect("/menu/")
    return redirect('/login/')

@app.route('/login/', methods=['post', 'get'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        account = mycursor.fetchone()
        if account:
            session['username'] = request.form.get('username')
            return redirect("/menu/")
        else:
            msg = 'Invalid Credentials. Please try again.'

    return render_template('ssis_login.html', msg=msg)

@app.route('/menu/')
def main():
    if not session.get("username"):
        return redirect("/login/")
    return render_template('ssis_main.html')

@app.route('/student_table/', methods=['post','get'])
def student_table():
    mycursor.execute('SELECT * FROM student_info')
    data = mycursor.fetchall()
    mycursor.execute('SELECT * FROM course')
    fill = mycursor.fetchall()
    return render_template('student_table.html', data=data, fill=fill)

@app.route('/student_table/add/', methods=['post','get'])
def add_student():
    mycursor.execute('SELECT `Course Name` FROM course')
    data = mycursor.fetchall()
    if request.method == 'POST' and 'student_id' in request.form:
        student_id = request.form['student_id']
        name = request.form['name']
        year_level = request.form['year_level']
        gender = request.form['gender']
        course = request.form['course']
        mycursor.execute("INSERT INTO `student_info` (`Student ID`, `Name`, `Year Level`, `Gender`, `Course`) "
                         "VALUES (%s,%s,%s,%s,%s)",
                         (student_id, name, year_level, gender, code2))
        db.commit()
        return redirect("/student_table/")
    else:
        pass
    return render_template('student_add.html', data=data)

@app.route('/student_table/edit', methods=['post', 'get'])
def edit_student():
    if request.method == 'POST' and "student_id" in request.form:
        student_id = request.form['student_id']
        name = request.form['name']
        year_level = request.form['year_level']
        gender = request.form['gender']
        course = request.form['course']
        query2 = f"UPDATE `student_info` SET `Student ID` = '{student_id}', `Name` = '{name}', `Year Level` = '{year_level}', `Gender` ='{gender}', `Course` = '{course}' WHERE `Student ID` = '{student_id}'"
        mycursor.execute(query2)
        db.commit()
        return redirect("/student_table/")
    return redirect("/student_table/")

@app.route('/course_table/add/', methods=['post','get'])
def add_course():
    mycursor.execute('SELECT `Name` FROM college')
    data = mycursor.fetchall()
    if request.method == 'POST' and 'course_code' in request.form:
        course_code = request.form['course_code']
        course = request.form['course']
        college = request.form['college']
        f = f"SELECT `Name` FROM college WHERE `Name` = '{college}'"
        mycursor.execute(f)
        code = mycursor.fetchone()
        code2 = code[0]
        mycursor.execute("INSERT INTO `course` (`Course Code`, `Course`, `College`) "
                         "VALUES (%s,%s,%s)",
                         (course_code, course, code2))
        db.commit()
        return redirect("/course_table/")
    else:
        pass
    return render_template('course_add.html', data=data)

@app.route('/course_table/edit', methods=['post', 'get'])
def edit_course():
    if request.method == 'POST' and "code" in request.form:
        code = request.form['code']
        name = request.form['name']
        college = request.form['college']

        query2 = f"UPDATE `course` SET `Course Code` = '{code}', `Course` = '{name}', `College` = '{college}' WHERE `Course Code` = '{code}'"
        mycursor.execute(query2)
        db.commit()
        return redirect("/course_table/")
    return redirect("/course_table/")

@app.route('/college_table/edit', methods=['post', 'get'])
def edit_college():
    if request.method == 'POST' and "code" in request.form:
        code = request.form['code']
        name = request.form['name']

        query2 = f"UPDATE `college` SET `Code` = '{code}', `Name` = '{name}' WHERE `Code` = '{code}'"
        mycursor.execute(query2)
        db.commit()
        return redirect("/college_table/")
    return redirect("/college_table/")

@app.route('/college_table/add/', methods=['post','get'])
def add_college():
    if request.method == 'POST' and 'college_code' in request.form:
        college_code = request.form['college_code']
        college = request.form['college']
        mycursor.execute("INSERT INTO `college` (`Code`, `Name`) "
                         "VALUES (%s,%s)",
                         (college_code, college))
        db.commit()
        return redirect("/college_table/")
    else:
        pass
    return render_template('college_add.html')

@app.route('/student_table/delete', methods=['post'])
def delete_student():
    if request.method == 'POST':
        student_id = request.form['currentRow']
        f = f"DELETE FROM student_info WHERE `Student ID` = '{student_id}'"
        mycursor.execute(f)
    return student_id

@app.route('/college_table/delete', methods=['post'])
def delete_college():
    if request.method == 'POST':
        college_code = request.form['currentRow']
        f = f"DELETE FROM college WHERE `Code` = '{college_code}'"
        mycursor.execute(f)
    return college_code

@app.route('/course_table/delete', methods=['post'])
def delete_course():
    if request.method == 'POST':
        course_code = request.form['currentRow']
        f = f"DELETE FROM course WHERE `Course Code` = '{course_code}'"
        mycursor.execute(f)
    return course_code

@app.route('/course_table/', methods=['post','get'])
def course_table():
    mycursor.execute('SELECT * FROM course')
    data = mycursor.fetchall()
    mycursor.execute('SELECT * FROM college')
    fill = mycursor.fetchall()
    return render_template('course_table.html', data=data, fill=fill)

@app.route('/college_table/', methods=['post','get'])
def college_table():
    mycursor.execute('SELECT * FROM college')
    data = mycursor.fetchall()
    return render_template('college_table.html', data=data)

@app.route('/logout/', methods=['post'])
def logout():
    session["username"] = None
    return redirect("/")