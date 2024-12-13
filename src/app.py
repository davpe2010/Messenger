import json
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

usertf = {}

with open("src/users.json", encoding="UTF-8") as file_in1:
    users = json.load(file_in1)

with open("src/message.json", encoding="UTF-8") as file_in2:
    datas = json.load(file_in2)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def login():
    global userfrom
    if request.method == "POST" and users[request.form["username"]] == request.form["password"]:
        usertf[request.form["username"]] = None
        return redirect(url_for("messenger", user=request.form["username"]))
    else:
        return redirect(url_for("index"))

@app.route("/messenger/<user>", methods=["GET", "POST"])
def messenger(user):
    if usertf[user] == None:
        return render_template("search.html", userr=user)
    else:
        return render_template("messenger.html", USER=usertf[user], DATA=datas[user][usertf[user]], userr=user)

@app.route("/search/<userr>", methods=["GET", "POST"])
def search(userr):
    global userto
    if request.method == "POST" and request.form["user"] in users:
        usertf[userr] = request.form["user"]
    return redirect(url_for("messenger", user=userr))

@app.route("/get_message/<userr>", methods=["GET", "POST"])
def get_message(userr):
    if request.method == "POST":
        datas[userr][usertf[userr]] = datas[userr][usertf[userr]] + "\n" + userr + ":  " + request.form["message"]
        datas[usertf[userr]][userr] = datas[usertf[userr]][userr] + "\n" + userr + ":  " + request.form["message"]
        with open("src/message.json", "w", encoding="UTF-8") as file_out:
            json.dump(datas, file_out, ensure_ascii=False, indent=2)
    return redirect(url_for("messenger", user=userr))


if __name__ == "__main__":
    app.run(host="192.168.0.127")
