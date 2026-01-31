# Give tag for images
from PIL import Image
# from clip_interrogator import Config, Interrogator
from io import BytesIO

# Configuration for the CLIP Interrogator
# Using a smaller model for faster inference on CPU
# config = Config(clip_model_name="ViT-L-14/openai")

# Create a global instance of the Interrogator
# This will download the models on the first run
# ci = Interrogator(config)

def get_tags_for_image(artworkBuffer: BytesIO):
    """
    Analyzes an image using CLIP Interrogator and returns a list of tags.
    """
    # image_path = ""
    # if not os.path.exists(image_path):
    #     print(f"Error: Image file not found at {image_path}")
    #     return []

    print(f"AI Tagging: Analyzing Image")
    image = Image.open(artworkBuffer).convert('RGB')
    return ["lorem", "ipsum"]

    # Generate the prompt
    prompt = ci.interrogate(image) # type: ignore
    
    # The prompt is a single string, so we can split it into tags
    tags = [tag.strip() for tag in prompt.split(',')]
    
    print(f"Generated tags: {tags}")
    return tags