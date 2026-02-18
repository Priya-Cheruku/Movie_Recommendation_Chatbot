from flask import Flask, request, jsonify, render_template
from chatbot import chatbot_response

app = Flask(__name__)

# 👉 Home page (Frontend)
@app.route("/")
def home():
    return render_template("index.html")


# 👉 Chat API (Backend logic)
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = chatbot_response(user_input)

    if type(response) == str:
        return jsonify({"reply": response})
    else:
        movies = []
        for _, row in response.iterrows():
            movies.append(f"{row['Movie']} ⭐{row['Rating']} ({row['Genre']})")
        return jsonify({"reply": movies})


if __name__ == "__main__":
    app.run(debug=True)
