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
def hello():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)


