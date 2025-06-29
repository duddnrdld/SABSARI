from flask import Flask, render_template, request, redirect, url_for, session
import json, os, random

app = Flask(__name__)
app.secret_key = "sabsari-super-secret-key"

DATA_FILE = "data/users.json"
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

        user_id = session.get("user_id") or str(random.randint(100000, 999999))
        session["user_id"] = user_id

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        data[user_id] = {
            "name": name,
            "birth": birth,
            "gender": gender,
            "birth_time": birth_time
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

        session["named"] = True
        return redirect(url_for("greeting"))

    return render_template("name_input.html")

@app.route("/greeting")
def greeting():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("name_input"))

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # 🔒 user_id가 JSON에 없을 경우 처리
    if user_id not in data:
        session.clear()
        return redirect(url_for("name_input"))

    name = data[user_id]["name"]
    return render_template("greeting.html", name=name)

@app.route("/fortune")
def fortune():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("name_input"))

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    name = data[user_id]["name"]

    return render_template("fortune_loading.html", name=name)

@app.route("/result")
def result():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("name_input"))

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    name = data[user_id]["name"]

    love_score = random.randint(1, 100)
    social_score = random.randint(1, 100)
    money_score = random.randint(1, 100)
    total_score = round((love_score + social_score + money_score) / 3)

    def get_comment(score):
        if score >= 80:
            return "아주 좋은 하루가 될 거예요!"
        elif score >= 60:
            return "무난하고 기분 좋은 하루예요."
        elif score >= 40:
            return "작은 주의가 필요해요."
        else:
            return "주의가 필요한 하루입니다."

    return render_template("fortune_result.html",
        name=name,
        love_score=love_score,
        social_score=social_score,
        money_score=money_score,
        total_score=total_score,
        love_comment=get_comment(love_score),
        social_comment=get_comment(social_score),
        money_comment=get_comment(money_score),
        total_comment=get_comment(total_score)
    )

if __name__ == "__main__":
    app.run(debug=True)
