# app.py (Flask 백엔드 수정)
from flask import Flask, render_template, request, redirect, url_for, session
import json, os, random

app = Flask(__name__)
app.secret_key = "sabsari-secret-key"

DATA_FILE = "data/users.json"

# 초기 데이터 파일 생성
if not os.path.exists(DATA_FILE):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

@app.route("/", methods=["GET", "POST"])
def name_input():
    if session.get("named"):
        return redirect(url_for("greeting"))

    if request.method == "POST":
        name = request.form["name"]
        birth = request.form["birth"]
        gender = request.form["gender"]
        birth_time = request.form["birth_time"]

        session["name"] = name
        session["named"] = True

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        data["user"] = {
            "name": name,
            "birth": birth,
            "gender": gender,
            "birth_time": birth_time
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

        return redirect(url_for("greeting"))

    return render_template("name_input.html")

@app.route("/greeting")
def greeting():
    name = session.get("name", "사용자")
    return render_template("greeting.html", name=name)

@app.route("/fortune")
def fortune():
    name = session.get("name", "사용자")
    return render_template("fortune_loading.html", name=name)

@app.route("/result")
def result():
    name = session.get("name", "사용자")
    love = random.randint(1, 100)
    relation = random.randint(1, 100)
    money = random.randint(1, 100)
    total = round((love + relation + money) / 3)

    def comment(score):
        if score >= 85:
            return "아주 좋은 날이에요!"
        elif score >= 60:
            return "기분 좋은 하루가 될 거예요."
        else:
            return "조심해야 할 하루예요."

    return render_template("fortune_result.html",
        name=name,
        love=love,
        relation=relation,
        money=money,
        total=total,
        love_msg=comment(love),
        relation_msg=comment(relation),
        money_msg=comment(money),
        total_msg=comment(total)
    )

if __name__ == "__main__":
    app.run(debug=True)
