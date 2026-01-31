import os
from flask import Flask, render_template, request, redirect, url_for
from tag import get_tags_for_image

# Optional: Load environment variables for API keys
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Routes
@app.route('/')
def index():
    """
    Main page.
    """
    return render_template('main.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handles the artwork upload process.
    """
    if request.method == 'POST':   
        file = request.files["file"]
        print(file)
            
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # TAGGING ===
            tags = get_tags_for_image(filepath)
            print(f"Generated tags for {filename}: {tags}")
            
            return render_template('upload.html', message=f"File uploaded successfully! Tags: {', '.join(tags)}")

    return render_template('upload.html')

if __name__ == '__main__':
    # Creates the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
