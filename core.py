import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_tags_for_image(image_path):
    """
    Analyzes an image using Google Vision AI and returns a list of tags.
    """
    # This is where you would integrate with the Google Cloud Vision API client.
    # For now, we'll return mock data.
    print(f"AI Tagging (mock): Analyzing {image_path}")
    return ['mock_tag', 'art', 'painting', 'cool', 'abstract']

