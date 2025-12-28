from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("atm.db")

# ---------- USER ----------
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    acc = request.form["account"]
    pin = request.form["pin"]

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE account=? AND pin=?", (acc, pin))
    user = cur.fetchone()

    if user:
        session["user"] = acc
        return redirect("/dashboard")
    return "Invalid Login"

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT balance FROM users WHERE account=?", (session["user"],))
    balance = cur.fetchone()[0]

    return render_template("dashboard.html", balance=balance)

@app.route("/withdraw", methods=["POST"])
def withdraw():
    amount = int(request.form["amount"])
    acc = session["user"]

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET balance = balance - ? WHERE account=?", (amount, acc))
    db.commit()

    return redirect("/dashboard")

@app.route("/deposit", methods=["POST"])
def deposit():
    amount = int(request.form["amount"])
    acc = session["user"]

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET balance = balance + ? WHERE account=?", (amount, acc))
    db.commit()

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- ADMIN ----------
@app.route("/admin")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin_login", methods=["POST"])
def admin_do_login():
    if request.form["username"] == "admin" and request.form["password"] == "admin123":
        session["admin"] = True
        return redirect("/admin_dashboard")
    return "Admin Login Failed"

@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    return render_template("admin_dashboard.html", users=users)

@app.route("/add_user", methods=["POST"])
def add_user():
    acc = request.form["account"]
    pin = request.form["pin"]
    bal = request.form["balance"]

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (acc, pin, bal))
    db.commit()

    return redirect("/admin_dashboard")

if __name__ == "__main__":
    app.run(debug=True)
