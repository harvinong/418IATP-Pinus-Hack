from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for
from entities.art import *
from entities.user import *
from tag import get_tags_for_image

app = Flask(__name__)
# UPLOAD_FOLDER = os.path.join('static', 'uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Routes
@app.route('/')
def index():
    """
    Main page.
    """
    return render_template('main.html')

@app.get("/user/")
def selfUserPage():
    return "Hello, user! :3"

@app.get("/user/@<user>")
def userPage(user:str):
    userInstance = User.findItem(user.lower())
    if not userInstance:
        return "404 Not Found"
    
    return render_template("userPage.html", userInstance = userInstance)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handles the artwork upload process.
    """
    if request.method == 'POST':   
        username = request.form["artist"]
        artist = User.findItem(username)
        pprint(artist)

        if artist is None:
            return render_template('upload.html', message=f"@{username.lower()} is not in the database")

        file = request.files["file"]
            
        if file:
            # filename = file.filename
            # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # file.save(filepath)
            imageBuffer: BytesIO = file.stream # type: ignore
            if not file.filename:
                return render_template('upload.html', message=f"Image filename is invalid.")
            extension: str = file.filename.split(".")[-1]
            blobResponse = uploadArt(artist, imageBuffer, extension)

            # TAGGING ===
            tags = get_tags_for_image(imageBuffer)
            print(f"Generated tags for {blobResponse.get("pathname")}: {tags}")
            
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
