from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "123"


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        con = sqlite3.connect("ContactApp.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query = "SELECT * FROM users WHERE email = ? and password = ?;"
        cur.execute(query, (email, password))
        data = cur.fetchone()

        if data:
            session["email"] = data["email"]
            session["password"] = data["password"]
            session["username"] = data["username"]
            session["id"] = data["id"]
            return redirect(url_for("home"))
        else:
            flash("Email and Password mismatch", "danger")

        return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            con = sqlite3.connect("ContactApp.db")
            cur = con.cursor()
            query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?);"
            cur.execute(query, (username, email, password))
            con.commit()
            flash("Registration successful", "success")

        except:
            flash("Registration unsuccessful", "danger")

        finally:
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route('/addContact', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        name = request.form["name"]
        number = request.form["number"]

        con = sqlite3.connect("ContactApp.db")
        cur = con.cursor()
        query = "INSERT INTO contact (id, name, number) VALUES (?, ?, ?);"
        cur.execute(query, (session["id"], name, number))
        con.commit()
        flash("Contact added successfully", "success")

        return redirect(url_for("home"))

    return render_template("addContact.html")


@app.route('/home')
def home():
    con = sqlite3.connect("ContactApp.db")
    cur = con.cursor()
    query = f"SELECT cid, name, number FROM contact WHERE id = {session['id']};"
    cur.execute(query)
    res = cur.fetchall()
    return render_template("home.html", datas=res)


@app.route('/editContact/<string:cid>', methods=['GET', 'POST'])
def editContact(cid):
    con = sqlite3.connect("ContactApp.db")
    if request.method == 'POST':
        name = request.form["name"]
        number = request.form["number"]

        con = sqlite3.connect("ContactApp.db")
        cur = con.cursor()
        query = "UPDATE contact SET name = ?, number = ? WHERE cid = ?;"
        cur.execute(query, (name, number, cid))
        con.commit()
        con.close()
        flash("Successfully saved", 'success')

        return redirect(url_for("home"))

    cur = con.cursor()
    query = f"SELECT name, number FROM contact WHERE cid = {cid};"
    cur.execute(query)
    res = cur.fetchone()
    return render_template("editContact.html", datas=res)


@app.route('/deleteContact/<string:cid>')
def deleteContact(cid):
    con = sqlite3.connect("ContactApp.db")
    cur = con.cursor()
    query = f"DELETE FROM contact WHERE cid = {cid};"
    cur.execute(query)
    con.commit()
    con.close()
    flash("Contact deleted successful", "success")

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0')
