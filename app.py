from flask import Flask, render_template
from flaskwebgui import FlaskUI

app: Flask = Flask(__name__)

@app.get("/")
def index():
    return render_template("main.html")

@app.get("/<nonexistent>")
def notFound(nonexistent):
    return f"<h1>404 Not Found</h1><p>\"{nonexistent}\" does not exist.</p><p>Please consider going outside and touching grass!</p>"

if __name__ == "__main__":
    ui: FlaskUI = FlaskUI(app = app, server = "flask")
    ui.run()