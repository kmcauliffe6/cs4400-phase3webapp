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
    return render_template('register.html')

@app.route('/register_visitor')
def register_visitor():
    return render_template('register_visitor.html')

@app.route('/register_employee')
def register_employee():
    return render_template('home.html')

@app.route('/register_employee_visitor')
def register_employee_visitor():
    return render_template('home.html')

#login methods
@app.route('/login', methods=['GET','POST'])
def login():
    #currently checking username and password, need to write queries to check
    #email and password
    if (request.method == 'POST'):
        sql = ("SELECT Username FROM User WHERE Username = '{email}' AND Password = '{password}';"
            .format(email=request.form['email'], password=request.form['password']))
        result = cursor.execute(sql);
        if result: #if any rows returned aka username was found
            row = cursor.fetchone()
            session['email'] = row.get('email')
            return render_template('user_functionality.html')
        else:
            return "Incorrect Credentials. Go back and try again"

if __name__ == "__main__":
    app.secret_key = 'supersecretkey'
    app.run(debug=True)


""""sql = "SELECT username FROM User WHERE username = 'lara'"
    result = cursor.execute(sql)
    answer = ""
    for row in cursor:
        answer += row['username']
"""



