from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g

import sqlite3
import urllib.request

connect_database = sqlite3.connect("loginInfo.db", check_same_thread=False)
database = connect_database.cursor()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        database.execute("INSERT INTO logins VALUES (?,?)", ( str(request.form["username"]), str(request.form["password"])))
        connect_database.commit()
        debug()
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        for row in database.execute("SELECT * FROM logins"):
            if request.form["username"] == row[0] and request.form["password"] == row[1]:
                return "<h1>YOU ARE LOGGED IN</h1>"
    return render_template("login.html")

@app.route("/admin/debug")
def debug():
    print("\n".join(list([str(row[0]) + "   " + str(row[1]) for row in database.execute("SELECT * FROM logins")])))
    return "debug"


def createDatabase():
    database.execute("CREATE TABLE logins (username text, password text)")

def deleteDatabase():
    database.execute("DELETE FROM logins")

@app.route("/admin/remake   ")
def remakeDatabase():
    deleteDatabase()
    createDatabase()

if __name__ == "__main__":
    app.run(debug=True)
    #remakeDatabase()
    # debug()
    # print("test")
    #deleteDatabase()
    #http://127.0.0.1:5000/
