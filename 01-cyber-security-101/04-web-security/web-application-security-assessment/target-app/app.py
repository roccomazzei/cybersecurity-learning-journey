from flask import Flask, request
import sqlite3

app = Flask(__name__)
DB = "lab.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    """)
    conn.execute("DELETE FROM users")
    conn.executemany(
        "INSERT INTO users(username,password,email) VALUES(?,?,?)",
        [
            ("admin", "password123", "admin@lab.local"),
            ("alice", "wonderland", "alice@lab.local"),
            ("bob", "football", "bob@lab.local")
        ]
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return """
    <h1>Lab 03 - Vulnerable Web Application</h1>
    <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/search?q=admin">User Search</a></li>
    </ul>
    """


@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /admin\n", 200, {"Content-Type": "text/plain"}


@app.route("/admin")
def admin():
    return "<h1>Administration Panel</h1><p>Restricted area</p>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
        """
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    conn = sqlite3.connect(DB)
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()
    if user:
        return "Welcome " + username
    return "Invalid credentials"


@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = sqlite3.connect(DB)
    sql = f"SELECT username,email FROM users WHERE username LIKE '%{q}%'"
    try:
        results = conn.execute(sql).fetchall()
    except Exception as e:
        results = [("SQL Error", str(e))]
    conn.close()
    output = "<h1>Search results</h1>"
    for row in results:
        output += f"<p>{row[0]} - {row[1]}</p>"
    return output


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)
