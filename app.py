from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from entities.art import *
from entities.user import *
from entities.countries import COUNTRIES
from entities.collection import CLIENT
from tag import get_tags_for_image
from bson.objectid import ObjectId
from datetime import datetime
from hashlib import sha256

app = Flask(__name__)
# Reference: https://www.geeksforgeeks.org/python/how-to-use-flask-session-in-python-flask/
# https://stackoverflow.com/questions/72025723/how-to-configure-mongodb-for-flask-session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_MONGODB"] = CLIENT
app.config["SESSION_MONGODB_DB"] = 'JalaArtMarket'
app.config["SESSION_MONGODB_COLLECTION"] = 'sessions'
Session(app)

# Middlewares
def matchpath(path: str, routes: list[str]):
    return path in routes or path in [route[:-1] if route[-1] == "/" else route + "/" for route in routes]

def visitPreviousUrl():
    visiting = session.get("visiting", None)
    return redirect(visiting) if visiting and not matchpath(visiting, ["/login/"]) else redirect("/user")

@app.after_request
def authenticate(req):
    if not matchpath(request.path, ["/", '/home/', "/login/", "/logout/", "/register/"]) and \
        not request.path.startswith("/static/") and \
        session.get("username") in [None, ""]:
        # print("Authentication in progress")
        print(session)
        return redirect("/login/")
    elif matchpath(request.path, ["/login/", "/register/"]) and session.get("username"):
        # print("Redirecting to user")
        print(session.get("visiting"), request.path)
        return redirect("/user/")
    # print("Going to", request.path)
    return req

@app.before_request
def trackVisitUrl():
    # print("trackVisitUrl", request.path)
    if not matchpath(request.path, ["/", '/home/', "/login/", "/logout/", "/register/", "/user/edit/", "/user/delete/"]) and \
        not request.path.startswith("/static/"):
        session["visiting"] = request.path
        print("trackVisitUrl()", session.get("visiting"))

def hashPassword(password: str):
    password = request.form["password"]
    passHash = sha256(password.encode())
    print(passHash.hexdigest())
    return passHash.hexdigest()

# Routes
@app.route('/')
@app.route('/home')
def index():
    """
    Main page.
    """
    return render_template('main.html', session = session.get("username"))

# Session Management
@app.route('/register/', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        password: str = request.form["password"].strip()
        confirm: str = request.form["password"].strip()

        if password != confirm:
            return render_template("registration.html", countries = COUNTRIES, error = "password and confirmation does not match.")
        
        username: str = request.form["username"].lower().strip()

        if User.findItem(username):
            return render_template("registration.html", countries = COUNTRIES, error = "username exists!")

        fullname: str = request.form["fullName"].strip()
        surname: str = request.form["surname"].strip()
        country: str|None = request.form["country"]
        country = country if country != "unspecified" else None
        website: str|None = request.form["website"]
        website = website.strip() if website != "" else None
        passhash: str = hashPassword(password)

        User(username, passhash, fullname, surname, country = country, website = website)

        return redirect("/login")
    
    return render_template("registration.html", countries = COUNTRIES)

@app.route('/login/', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].lower().strip()
        passhash = hashPassword(request.form["password"]).strip()
        
        userInstance = User.findItem(username)
        if userInstance and userInstance.passHash == passhash:
            # record username and passHash in session
            session["username"] = username
            print(session.get("username"))
            visitPreviousUrl()
        else:
            return render_template("login.html", status = "fail")

    return render_template("login.html")

@app.get("/logout/")
def logout():
    session.clear()
    return render_template("logout.html")

# User Management
def getUser(user: str|None = None) -> User|None:
    if user is None:
        username = session.get("username")
        if not username: return
    else:
        username = user.lower()
    userInstance = User.findItem(username)
    return userInstance

@app.get("/user/@<user>/")
@app.get("/user/")
def userPage(user:str|None = None):
    userInstance = getUser(user)
    if not userInstance:
        return "404 Not Found"
    print(session.get("username"), userInstance.username)
    return render_template("userPage.html", userInstance = userInstance, inSession = session.get('username') == userInstance.username)

@app.route("/user/edit/", methods = ["GET", "POST"])
def editUser():
    userInstance = getUser()
    if not userInstance:
        return not_found()
    
    if request.method == "POST":
        userInstance = getUser()
        if not userInstance:
            return render_template("editUser.html", userInstance = userInstance, countries = COUNTRIES, error = "user does not exist!")
        
        oldUsername: str = userInstance.username
        newUsername: str = request.form["username"].lower().strip()

        print(oldUsername, newUsername, oldUsername != newUsername)
        if oldUsername != newUsername and User.findItem(newUsername):
            return render_template("editUser.html", userInstance = userInstance, countries = COUNTRIES, error = "username exists!")


        passhash: str = hashPassword(request.form["password"])
        if passhash != userInstance.passHash:
            return render_template("editUser.html", userInstance = userInstance, countries = COUNTRIES, error = "Password does not match!")

        # Get changes
        userInstance.username = newUsername
        userInstance.fullName = request.form["fullName"].strip()
        userInstance.surName = request.form["surname"].strip()
        country: str|None = request.form["country"]
        userInstance.country = country if country != "unspecified" else None
        website: str|None = request.form["website"]
        userInstance.website = website.strip() if website != "" else None

        # Save changes
        userInstance.update()

        return redirect("/user")

    print("editUser() -> ", session.get("visiting"))
    return render_template("editUser.html", userInstance = userInstance, countries = COUNTRIES)

@app.route("/user/delete/", methods = ["GET", "POST"])
def deleteUser():
    userInstance = getUser()
    if not userInstance:
        return not_found()
    
    if request.method == "POST":
        userInstance = getUser()
        if not userInstance:
            return render_template("deleteUser.html", userInstance = userInstance, countries = COUNTRIES, error = "user does not exist!")

        print(request.form.get("confirm"))
        if request.form.get("confirm") != 'yes':
            return render_template("deleteUser.html", userInstance = userInstance, countries = COUNTRIES, error = "You must confirm your decision!")

        passhash: str = hashPassword(request.form["password"])
        if passhash != userInstance.passHash:
            return render_template("deleteUser.html", userInstance = userInstance, countries = COUNTRIES, error = "Password does not match!")
        
        userInstance.deleteItem(passhash)

        return redirect("/logout")
    
    return render_template("deleteUser.html", userInstance = userInstance)

# Art Management
@app.get("/user/@<user>/creations/")
@app.get("/user/@<user>/creation/")
@app.get("/user/creations/")
@app.get("/user/creation/")
def userCreationPage(user: str|None = None):
    userInstance = getUser(user)
    if not userInstance:
        return "404 Not Found"
    
    artInstances = Art.findArtsFromArtist(userInstance._id) # type: ignore
    
    return render_template(
        "creations.html",
        userInstance = userInstance,
        artInstances = artInstances
        )

@app.get("/creations/")
@app.get("/creation/")
def allCreationsPage():
    artInstances = Art.getAllArts()

    table: dict[Art, User|None] = {}
    for artInstance in artInstances:
        artistID = artInstance.artistID
        if artistID is None:
            table[artInstance] = None
        else:
            artistInstance = User.findItemByID(artistID)
            table[artInstance] = artistInstance

    return render_template(
        "creations.html",
        artInstances = table,
        userInstance = "all"
    )

@app.get("/art/<id>/")
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

@app.route('/art/upload/', methods=['GET', 'POST'])
def upload():
    """
    Handles the artwork upload process.
    """
    username = session["username"]
    if request.method == 'POST':
        # Form fields
        title = request.form["title"].strip()
        desc = request.form["desc"].strip()
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
            artInstance = Art(title, desc, blobResponse["url"], int(price.replace(".", "")), tags = userDefTags + tags, artistID = artist._id)
            
            return render_template(
                'upload.html', 
                message=f"File uploaded successfully! Tags: {', '.join(tags)}",
                imageName = blobResponse.get("pathname"),
                artID = artInstance._id)

    return render_template('upload.html', username = username)

# Not Found (404)
@app.errorhandler(404)
def not_found(err = None):
    if request.path.islower():
        return render_template("notfound.html")
    else:
        return redirect(request.path.lower())

if __name__ == '__main__':
    # Creates the upload folder if it doesn't exist
    # if not os.path.exists(UPLOAD_FOLDER):
    #     os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
