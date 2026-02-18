from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from chatbot import chatbot_response

app = Flask(__name__)
app.secret_key = "movie_secret_key"

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            session["user"] = username
            return redirect(url_for("chatpage"))

    return render_template("login.html")

@app.route("/chatpage")
def chatpage():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html", username=session["user"])

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = chatbot_response(user_input)

    if isinstance(response, list):
        return jsonify({"type": "movies", "movies": response})
    else:
        return jsonify({"type": "text", "reply": response})

# 👇 NEW LOGOUT ROUTE
@app.route("/logout")
def logout():
    session.pop("user", None)
    return render_template("goodbye.html")



if __name__ == "__main__":
    app.run(debug=True)
