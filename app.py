from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/scrap', methods = ['POST'])
def scrap_comments():
    return render_template('index.html')