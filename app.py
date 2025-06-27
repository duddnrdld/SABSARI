from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

DATA_FILE = "data/users.json"

# 간단한 JSON DB 초기화
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)


@app.route("/", methods=["GET", "POST"])
def name_input():
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