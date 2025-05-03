from agents import ImageGenAgent
from PIL import Image

async def chat_response(prompt: str):
    """
    Streams the response (text + image) from the model.
    """
    api_key = "AIzaSyCc0FzAq-hUkzg2RwB0hASbRDM5E2dVpcQ"
    agent = ImageGenAgent(api_key=api_key)

    response_text, image = agent.generate_image_response(prompt)

    if response_text:
        yield response_text
    if image:
        yield image
