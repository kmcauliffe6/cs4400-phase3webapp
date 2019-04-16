import pymysql
from flask import Flask, request, render_template, redirect, url_for, flash, session

app = Flask(__name__)
connection = pymysql.connect(host='localhost',
                             user='root',
                             passwd='13',
                             db='phase3data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

@app.route("/")
def setup():
    return render_template('home.html')

#registration methods
@app.route('/registernavigation')
def registernavigation():
    return render_template('register_navigation.html')

@app.route('/back')
def back_to_home():
    return render_template('home.html')

@app.route('/register_user')
def register_user():
    return render_template('home.html')

@app.route('/register_visitor')
def register_visitor():
    return render_template('home.html')

@app.route('/register_employee')
def register_employee():
    return render_template('home.html')

@app.route('/register_employee_visitor')
def register_employee_visitor():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)


""""sql = "SELECT username FROM User WHERE username = 'lara'"
    result = cursor.execute(sql)
    answer = ""
    for row in cursor:
        answer += row['username']
"""



