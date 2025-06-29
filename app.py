```python
from flask import Flask, render_template, request, redirect, url_for, session
import json, os, random

app = Flask(__name__)
app.secret_key = "sabsari-super-secret-key"

DATA_FILE = "data/users.json"
COMMENTS_FILE = "data/fortune_comments.json"

# Ensure data file exists
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
    love_score = random.randint(1, 100)
    relation_score = random.randint(1, 100)
    money_score = random.randint(1, 100)
    total_score = round((love_score + relation_score + money_score) / 3)

    with open(COMMENTS_FILE, "r") as f:
        comments_data = json.load(f)

    def get_comment(score, category):
        if score <= 20:
            return comments_data[category]["0"]
        elif score <= 40:
            return comments_data[category]["20"]
        elif score <= 60:
            return comments_data[category]["40"]
        elif score <= 80:
            return comments_data[category]["60"]
        else:
            return comments_data[category]["80"]

    love_comment = get_comment(love_score, "love")
    relation_comment = get_comment(relation_score, "relation")
    money_comment = get_comment(money_score, "money")
    total_comment = get_comment(total_score, "total")

    user_id = session.get("user_id")
    name = ""
    if user_id:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        name = data.get(user_id, {}).get("name", "")

    return render_template(
        "fortune_result.html",
        name=name,
        love_score=love_score,
        relation_score=relation_score,
        money_score=money_score,
        total_score=total_score,
        love_comment=love_comment,
        relation_comment=relation_comment,
        money_comment=money_comment,
        total_comment=total_comment
    )

if __name__ == "__main__":
    app.run(debug=True)
```