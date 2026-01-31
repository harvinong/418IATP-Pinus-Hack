import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from core import allowed_file, get_tags_for_image

# Optional: Load environment variables for API keys
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
# A secret key is needed for session management
app.config['SECRET_KEY'] = 'your-super-secret-key' # Replace with a real secret key
# Folder to store uploaded images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Database Setup (Placeholder) ---
# For a hackathon, we can start without the full DB implementation
# and add it later. This keeps things simple initially.
# e.g., using Flask-SQLAlchemy

# --- Routes ---
@app.route('/')
def index():
    """
    Main page, displays the gallery of uploaded art.
    """
    # In the future, this will fetch artwork from the database.
    # For now, we can scan the uploads folder to display images.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    artworks = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in os.listdir(app.config['UPLOAD_FOLDER'])]
    
    # We'll create a simple list of dicts to pass to the template
    artwork_data = [{'path': url_for('static', filename=f'uploads/{os.path.basename(p)}'), 'title': 'Untitled'} for p in artworks]

    return render_template('index.html', artworks=artwork_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handles the artwork upload process.
    """
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url) # Or show an error
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # --- AI Tagging Step ---
            tags = get_tags_for_image(filepath)
            print(f"Generated tags for {filename}: {tags}")

            # --- Database Step (Placeholder) ---
            # Here you would save the file path, title, price, and tags to the DB.
            # e.g., new_artwork = Artwork(title=request.form['title'], filepath=filepath, tags=tags)
            # db.session.add(new_artwork)
            # db.session.commit()
            
            return redirect(url_for('index'))

    return render_template('upload.html')

if __name__ == '__main__':
    # Creates the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
