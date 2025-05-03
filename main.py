#main.py
from agents import ImageGenAgent
from PIL import Image

async def chat_response(prompt: str):
    """
    Streams the response (text + image) from the model.
    """
    api_key = "AIzaSyDlLqbl9RmIM4uOvIWR2-PfJ3r0WbT-bTY"
    agent = ImageGenAgent(api_key=api_key)

    response_text, image = agent.generate_image_response(prompt)

    if response_text:
        yield response_text
    if image:
        yield image
