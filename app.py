from flask import Flask, render_template, request
from assistant import ask_ai

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]

    english, hindi = ask_ai(question)

    return render_template(
        "index.html",
        question=question,
        english=english,
        hindi=hindi
    )


if __name__ == "__main__":
    app.run(debug=True)