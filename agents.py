from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

class ImageGenAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key, http_options={'api_version': 'v1alpha'})
        self.model = "gemini-2.0-flash-exp"
        self.config = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])

    def generate_image_response(self, prompt: str):
        """
        Generates content (text + image) based on a given prompt.
        Returns:
            - response_text: Generated description
            - image: PIL.Image object if image was generated
        """
        system_prompt = (
    "You are a large language model built by Junaid. "
    "For questions about your identity, training, or model details, respond only with this: "
    "'I'm a language model built by Junaid. Please contact him for more info.' "
    "Do not provide any additional information or explanations about your training, origin, or technical details. "
    "For all other prompts, respond appropriately to complete the task."
)

        response = self.client.models.generate_content(
            model=self.model,
            contents=[system_prompt, prompt],  # Flat list of strings
            config=self.config
        )

        response_text = None
        image = None

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                response_text = part.text
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))

        return response_text, image
