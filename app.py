from flask import Flask, render_template, request, redirect, url_for, session
import json, os, random

app = Flask(__name__)
app.secret_key = "sabsari-super-secret-key"

DATA_FILE = "data/users.json"

if not os.path.exists(DATA_FILE):
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

        session["named"] = True
        session["name"] = name
        return redirect(url_for("greeting"))

    return render_template("name_input.html")

@app.route("/greeting")
def greeting():
    name = session.get("name", "삽사리")
    return render_template("greeting.html", name=name)

@app.route("/fortune")
def fortune():
    name = session.get("name", "삽사리")
    return render_template("fortune_loading.html", name=name)

@app.route("/result")
def result():
    name = session.get("name", "삽사리")

    love = random.randint(1, 100)
    social = random.randint(1, 100)
    money = random.randint(1, 100)
    average = round((love + social + money) / 3)

    def comment(score):
        if score >= 80:
            return "아주 좋은 날이에요!"
        elif score >= 60:
            return "기분 좋은 하루가 될 거예요."
        elif score >= 40:
            return "작은 주의가 필요해요."
        else:
            return "조심해야 할 하루예요."

    comments = {
        "love_comment": comment(love),
        "social_comment": comment(social),
        "money_comment": comment(money),
        "total_comment": comment(average),
    }

    return render_template(
        "fortune_result.html",
        name=name,
        love=love,
        social=social,
        money=money,
        average=average,
        **comments
    )

if __name__ == "__main__":
    app.run(debug=True)
