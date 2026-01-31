from flask import Flask, render_template, url_for

app: Flask = Flask(__name__)

@app.get("/")
def index():
    return render_template("main.html")

@app.get("/user")
def selfUser():
    return "Hello, user! :3"

@app.get("/@<user>")
def user(user:str):
    return f"Hello, {user}!"

@app.get("/<nonexistent>")
def notFound(nonexistent):
    return f"<h1>404 Not Found</h1><p>\"{nonexistent}\" does not exist.</p><p>Please consider going outside and touching grass!</p>"

if __name__ == "__main__":
    app.run(debug = True)