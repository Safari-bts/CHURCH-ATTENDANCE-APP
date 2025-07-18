from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import json
import os
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your-secret-key'

DATA_FILE = 'attendance.json'
USERS_FILE = 'users.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE) as f:
        users = json.load(f)
        for user in users:
            if not user["password"].startswith("pbkdf2:sha256"):
                user["password"] = generate_password_hash(user["password"])
        return users

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        for user in users:
            if user["username"] == username and check_password_hash(user["password"], password):
                session["user"] = user["username"]
                session["role"] = user["role"]
                flash("Login successful!", "success")
                return redirect(url_for("index"))

        flash("Invalid username or password", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" not in session or session.get("role") != "admin":
        flash("Only admins can register new users.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        new_user = {
            "username": request.form["username"],
            "password": generate_password_hash(request.form["password"]),
            "role": request.form["role"]
        }
        users = load_users()
        if any(u["username"] == new_user["username"] for u in users):
            flash("Username already exists.", "warning")
            return redirect(url_for("register"))

        users.append(new_user)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
            flash("New user registered successfully!", "success")
        return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        data = load_data()
        new_record = {
            "date": request.form['date'],
            "service": request.form['service'],
            "males": int(request.form['males']),
            "females": int(request.form['females']),
            "children": int(request.form['children']),
            "total": int(request.form['males']) + int(request.form['females']) + int(request.form['children']),
            "recorded_by": session["user"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(new_record)
        save_data(data)
        flash("Attendance recorded successfully!", "success")
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/records")
def records():
    if "user" not in session:
        return redirect(url_for("login"))

    data = load_data()
    totals = {
        "males": sum(d['males'] for d in data),
        "females": sum(d['females'] for d in data),
        "children": sum(d['children'] for d in data),
        "overall": sum(d['total'] for d in data)
    }
    return render_template("records.html", records=data, totals=totals)

@app.route("/edit/<int:record_id>", methods=["GET", "POST"])
def edit(record_id):
    if "user" not in session or session.get("role") != "admin":
        flash("You are not authorized to edit records.", "danger")
        return redirect(url_for("records"))

    data = load_data()
    if request.method == "POST":
        data[record_id] = {
            "date": request.form['date'],
            "service": request.form['service'],
            "males": int(request.form['males']),
            "females": int(request.form['females']),
            "children": int(request.form['children']),
            "total": int(request.form['males']) + int(request.form['females']) + int(request.form['children']),
            "recorded_by": session["user"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_data(data)
        flash("Attendance updated successfully!", "info")
        return redirect(url_for("records"))

    return render_template("edit.html", record=data[record_id], record_id=record_id)

@app.route("/delete/<int:record_id>")
def delete(record_id):
    if "user" not in session or session.get("role") != "admin":
        flash("You are not authorized to delete records.", "danger")
        return redirect(url_for("records"))

    data = load_data()
    if 0 <= record_id < len(data):
        data.pop(record_id)
        save_data(data)
        flash("Record deleted successfully.", "warning")
    return redirect(url_for("records"))

@app.route("/export")
def export():
    if "user" not in session:
        return redirect(url_for("login"))

    data = load_data()
    if not data:
        flash("No data to export", "warning")
        return redirect(url_for("records"))

    df = pd.DataFrame(data)
    excel_file = "attendance_export.xlsx"
    df.to_excel(excel_file, index=False)
    return send_file(excel_file, as_attachment=True)

@app.route("/chart")
def chart():
    if "user" not in session:
        return redirect(url_for("login"))

    data = load_data()
    week_data = defaultdict(lambda: {"males": 0, "females": 0, "children": 0})

    for record in data:
        week = datetime.strptime(record["date"], "%Y-%m-%d").isocalendar()[1]
        week_data[week]["males"] += record["males"]
        week_data[week]["females"] += record["females"]
        week_data[week]["children"] += record["children"]

    weeks = sorted(week_data.keys())
    male_counts = [week_data[w]["males"] for w in weeks]
    female_counts = [week_data[w]["females"] for w in weeks]
    children_counts = [week_data[w]["children"] for w in weeks]

    return render_template("chart.html", weeks=weeks, males=male_counts, females=female_counts, children=children_counts)

if __name__ == "__main__":
    app.run(debug=True)
