from flask import Flask, render_template, request, send_from_directory
import nlp_model
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    res = nlp_model.get_response(msg)
    return res

# Serve the jasminelogo.png image file
@app.route("/static/jasminelogo.png")
def serve_image():
    return send_from_directory("static", "jasminelogo.png")

if __name__ == "__main__":
    app.run()