from flask import Flask, render_template, request, redirect, url_for, session, make_response
import sqlite3, uuid, os

app = Flask(__name__)
app.secret_key = "sabsari-super-secret-key"

DB_FILE = "data/users.db"

# DB 초기화
def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            birth TEXT,
            gender TEXT,
            birth_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 사용자 조회
def get_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# 사용자 등록
def save_user(user_id, name, birth, gender, birth_time):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (id, name, birth, gender, birth_time) VALUES (?, ?, ?, ?, ?)",
                   (user_id, name, birth, gender, birth_time))
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def name_input():
    user_id = request.cookies.get("user_id")
    user = get_user(user_id) if user_id else None

    if user:
        return redirect(url_for("greeting"))

    if request.method == "POST":
        name = request.form["name"]
        birth = request.form["birth"]
        gender = request.form["gender"]
        birth_time = request.form["birth_time"]

        new_user_id = str(uuid.uuid4())
        save_user(new_user_id, name, birth, gender, birth_time)

        resp = make_response(redirect(url_for("greeting")))
        resp.set_cookie("user_id", new_user_id, max_age=60*60*24*365)  # 1년
        return resp

    return render_template("name_input.html")


@app.route("/greeting")
def greeting():
    user_id = request.cookies.get("user_id")
    user = get_user(user_id)
    if not user:
        return redirect(url_for("name_input"))

    return render_template("greeting.html", name=user[1])


@app.route("/fortune")
def fortune():
    return render_template("fortune_loading.html")


@app.route("/result")
def result():
    import random
    score = random.randint(1, 100)
    return render_template("fortune_result.html", score=score)


if __name__ == "__main__":
    app.run(debug=True)
