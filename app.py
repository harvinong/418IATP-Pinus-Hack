from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from entities.art import *
from entities.user import *
from tag import get_tags_for_image
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
# Reference: https://www.geeksforgeeks.org/python/how-to-use-flask-session-in-python-flask/
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# UPLOAD_FOLDER = os.path.join('static', 'uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)

# Routes
@app.route('/')
def index():
    """
    Main page.
    """
    return render_template('main.html')

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        userInstance = User.findItem(username)
        if userInstance and userInstance.passHash == password:
            # record username and passHash in session
            session["username"] = username
            return redirect("/user")
        else:
            return render_template("login.html", status = "fail")

    return render_template("login.html")

@app.get("/logout")
def logout():
    session["username"] = None
    return redirect("/")

@app.before_request
def authenticate():
    if request.path not in ["/", "/login"] and \
        not request.path.startswith("/static/") and \
        not session.get("username"):
        return redirect("/login")

@app.get("/user")
def selfUserPage():
    username = session["username"]
    userInstance = User.findItem(username)
    if not userInstance:
        return "404 Not Found"
    
    return render_template("userPage.html", userInstance = userInstance)

@app.get("/user/@<user>")
def userPage(user:str):
    userInstance = User.findItem(user.lower())
    if not userInstance:
        return "404 Not Found"
    
    return render_template("userPage.html", userInstance = userInstance)

@app.get("/user/@<user>/creations")
def creationPage(user:str):
    userInstance = User.findItem(user.lower())
    if not userInstance:
        return "404 Not Found"
    
    artInstances = Art.findArtsFromArtist(userInstance._id) # type: ignore
    
    return render_template(
        "creations.html",
        userInstance = userInstance,
        artInstances = artInstances
        )

@app.get("/art/<id>")
def artPage(id: str):
    if not ObjectId.is_valid(id):
        return "Invalid id"
    
    artInstance = Art.findArt(ObjectId(id))
    if not artInstance:
        return "404 Not Found"
    
    userInstance = User.findItemByID(artInstance.artistID) if artInstance.artistID else None
    
    return render_template(
        "artwork.html", 
        artInstance = artInstance, 
        userInstance = userInstance,
        artAge = round(artInstance.getAge().total_seconds()/60))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handles the artwork upload process.
    """
    if request.method == 'POST':
        # Form fields
        username = request.form["artist"]
        title = request.form["title"]
        desc = request.form["desc"]
        price = request.form["price"]
        userDefTags = request.form["tags"].split()

        # Find artist
        artist = User.findItem(username)
        pprint(artist)
        if artist is None:
            return render_template('upload.html', message=f"@{username.lower()} is not in the database")

        file = request.files["file"]
            
        if file:
            # Uploading image to blob storage
            imageBuffer: BytesIO = file.stream # type: ignore
            if not file.filename:
                return render_template('upload.html', message=f"Image filename is invalid.")
            extension: str = file.filename.split(".")[-1]
            blobResponse = uploadArt(artist, imageBuffer, extension)

            # TAGGING ===
            tags = get_tags_for_image(imageBuffer)
            print(f"Generated tags for {blobResponse.get("pathname")}: {tags}")

            # Saving to database
            Art(title, desc, blobResponse["url"], int(price.replace(".", "")), tags = userDefTags + tags, artistID = artist._id)
            
            return render_template(
                'upload.html', 
                message=f"File uploaded successfully! Tags: {', '.join(tags)}",
                imageName = blobResponse.get("pathname"),
                imageLink = blobResponse.get("url"))

    return render_template('upload.html')

@app.get("/<nonexistent>")
def notFound(nonexistent):
    return f"<h1>404 Not Found</h1><p>\"{nonexistent}\" does not exist.</p><p>Please consider going outside and touching grass!</p>"

if __name__ == '__main__':
    # Creates the upload folder if it doesn't exist
    # if not os.path.exists(UPLOAD_FOLDER):
    #     os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
