from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import mysql.connector

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
        mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
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

@app.route('/student_table/', methods=['post'])
def student_table():
    mycursor.execute('SELECT * FROM student_info')
    data = mycursor.fetchall()
    return render_template('student_table.html', data=data)

@app.route('/course_table/', methods=['post'])
def college_table():
    mycursor.execute('SELECT * FROM course')
    data = mycursor.fetchall()
    return render_template('course_table.html', data=data)

@app.route('/college_table/', methods=['post'])
def course_table():
    mycursor.execute('SELECT * FROM college')
    data = mycursor.fetchall()
    return render_template('college_table.html', data=data)

@app.route('/logout/', methods=['post'])
def logout():
    session["username"] = None
    return redirect("/")