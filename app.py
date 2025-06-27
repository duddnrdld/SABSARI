from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "sabsari-super-secret-key"  # 세션을 위한 시크릿 키 설정


DATA_FILE = "data/users.json"

# 간단한 JSON DB 초기화
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)


@app.route("/", methods=["GET", "POST"])
def name_input():
    if session.get("named"):  # 이름 이미 지었으면 바로 /greeting 이동
        return redirect(url_for("greeting"))

    if request.method == "POST":
        name = request.form["name"]
        birth = request.form["birth"]
        gender = request.form["gender"]
        birth_time = request.form["birth_time"]

        # 저장
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

        session["named"] = True  # 이름 지은 기록 세션에 저장
        return redirect(url_for("greeting"))

    return render_template("name_input.html")


@app.route("/greeting")
def greeting():
    return render_template("greeting.html")


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
