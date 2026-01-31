# Give tag for images
from PIL import Image
from clip_interrogator import Config, Interrogator
import os

# Configuration for the CLIP Interrogator
# Using a smaller model for faster inference on CPU
config = Config(clip_model_name="ViT-L-14/openai")

# Create a global instance of the Interrogator
# This will download the models on the first run
ci = Interrogator(config)

def get_tags_for_image(image_path):
    """
    Analyzes an image using CLIP Interrogator and returns a list of tags.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return []

    print(f"AI Tagging: Analyzing {image_path}")
    image = Image.open(image_path).convert('RGB')
    
    # Generate the prompt
    prompt = ci.interrogate(image)
    
    # The prompt is a single string, so we can split it into tags
    tags = [tag.strip() for tag in prompt.split(',')]
    
    print(f"Generated tags: {tags}")
    return tags