import os
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route("/debug/run")
def run_command():
    cmd = request.args.get("cmd", "")
    return os.popen(cmd).read()

@app.route("/admin/query")
def admin_query():
    user_id = request.args.get("user_id", "")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    sql = "SELECT id, name, role FROM users WHERE id = " + user_id
    rows = cursor.execute(sql).fetchall()

    return {"rows": rows}

@app.route("/deploy/restart")
def restart_service():
    service = request.args.get("service", "default")
    subprocess.call("systemctl restart " + service, shell=True)
    return "ok"

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if username == "admin" and password == "admin123":
        return "login success"

    return "login failed"
