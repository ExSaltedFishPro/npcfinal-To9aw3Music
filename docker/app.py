import time
from flask import Flask, redirect, request, jsonify, render_template, send_file, make_response
import jwt
import uuid
import hashlib
import random
import os



def generate_codes():
    return "-".join(uuid.uuid4().hex[:4] for _ in range(5))

JWT_SECRET = uuid.uuid4().hex

userDB = {
    "anon": {"password": hashlib.md5(JWT_SECRET.encode()).hexdigest(), "perm": "admin", "balance": 10},
}

itemDB = [
    {"id": "01","name": "天球(そら)のMúsica", "music": "2689981077"},
    {"id": "02","name": "Imprisoned XII", "music": "2680457871"},
    {"id": "03","name": "KiLLKiSS", "music": "2653641752"},
]

commentsDB = [
    {"username": "喜欢捡石头的高木公火丁", "comment": "saki写的歌真好", "rating": 5, "reply": "谢谢支持"},
    {"username": "喜欢蓝毛", "comment": "和我回来组crychic吧", "rating": 5, "reply": "过去软弱的我已经死了"},
    {"username": "ANON TOKYO", "comment": "我抽到武道馆的票了哦！", "rating": 5, "reply": "好哦"},
    {"username": "苦瓜大王", "comment": "不会长久", "rating": 3, "reply": "亚达哟"},
]


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    token = request.cookies.get("Authorization")
    if token:
        print("token: "+token)
        try:
            datas  = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            username = datas.get("username")
            return render_template("index.html"
                                   ,username=username
                                   ,items=itemDB
                                   ,comments=commentsDB)
        except jwt.ExpiredSignatureError:
            resp = make_response(redirect("/login"))
            resp.set_cookie("Authorization", "")
            return resp
        except jwt.InvalidTokenError:
            resp = make_response(redirect("/login"))
            resp.set_cookie("Authorization", "")
            return resp
    else:
        return render_template("login.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/api/<action>", methods=["POST"])
def api(action):
    if action == "login":
        datas = request.get_json()
        username = datas.get("username")
        password = datas.get("password")
        if userDB.get(username) and userDB[username]["password"] == hashlib.md5(password.encode()).hexdigest():
            token = jwt.encode({"username": username, "perm": userDB[username]["perm"]}, JWT_SECRET, algorithm="HS256")
            resp = make_response(redirect("/"))
            resp.set_cookie("Authorization", token)
            if userDB[username]["perm"] == "admin":
                resp = make_response(redirect("/admin"))
                resp.set_cookie("Authorization", token)
                return resp
            return resp
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    elif action == "register":
        datas = request.get_json()
        username = datas.get("username")
        # security check
        for i in username:
            if not str.isalnum(i):
                return jsonify({"error": "Invalid username"}), 400
        password = datas.get("password")
        if userDB.get(username):
            return jsonify({"error": "User already exists"}), 400
        userDB[username] = {"password": hashlib.md5(password.encode()).hexdigest(), "perm": "customer", "balance": 0}
        return redirect("/login")
    elif action == "comment":
        if request.cookies.get("Authorization") == "":
            return jsonify({"error": "Unauthorized"}), 401
        token = request.cookies.get("Authorization")
        try:
            datas  = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            username = datas.get("username")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Unauthorized"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Unauthorized"}), 401
        datas = request.get_json()
        username = datas.get("username")
        comment = datas.get("comment")
        rating = datas.get("rating")
        if int(rating) <= 3:
            reply = random.choice(["我们会加油的"])
        else:
            reply = random.choice(["谢谢支持"])
        # security check
        for i in username:
            if not str.isalnum(i):
                return jsonify({"error": "Invalid username"}), 400
        if str(rating) not in ["1", "2", "3", "4", "5"]:
            return jsonify({"error": "Invalid rating"}), 400
        for i in comment:
            if i in ["{", "}", "[", "]", "&", "|", "$", "`", "*", "?", "!", "#", "%", "@"]:
                return jsonify({"error": "Invalid comment"}), 400
        commentsDB.append({"username": username, "comment": comment, "rating": rating, "reply": reply})
        return jsonify({"message": "Comment added"}), 200

@app.route("/play/<id>", methods=["GET"])
def play(id):
    token = request.cookies.get("Authorization")
    if token:
        try:
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            #check id
            n = 0
            for i in itemDB:
                if i["id"] == id:
                    break
                n += 1
            return render_template("play.html", item=itemDB[n])
        except jwt.ExpiredSignatureError:
            resp = make_response(redirect("/login"))
            resp.set_cookie("Authorization", "")
            return resp
        except jwt.InvalidTokenError:
            resp = make_response(redirect("/login"))
            resp.set_cookie("Authorization", "")
            return resp
    else:
        return redirect("/login")


@app.route("/logout", methods=["GET"])
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("Authorization", "")
    return resp

app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)