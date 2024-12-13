import json
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

userto = None
userfrom = None

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
        userfrom = request.form["username"]
        print("newuser")
        return redirect(url_for("messenger"))
    else:
        return redirect(url_for("index"))

@app.route("/messenger", methods=["GET", "POST"])
def messenger():
    if userto == None:
        return render_template("search.html")
    else:
        return render_template("messenger.html", USER=userto, DATA=datas[userfrom][userto])

@app.route("/search", methods=["GET", "POST"])
def search():
    global userto
    if request.method == "POST" and request.form["user"] in users:
        userto = request.form["user"]
    return redirect(url_for("messenger"))

@app.route("/get_message", methods=["GET", "POST"])
def get_message():
    if request.method == "POST":
        datas[userfrom][userto] = datas[userfrom][userto] + "\n" + userfrom + ":  " + request.form["message"]
        datas[userto][userfrom] = datas[userto][userfrom] + "\n" + userfrom + ":  " + request.form["message"]
        with open("src/message.json", "w", encoding="UTF-8") as file_out:
            json.dump(datas, file_out, ensure_ascii=False, indent=2)
    return redirect(url_for("messenger"))


if __name__ == "__main__":
    app.run()
