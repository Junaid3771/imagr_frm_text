from agents import ImageGenAgent
from unittest.mock import patch

def test_generate_image_response():
    agent = ImageGenAgent(api_key="dummy")
    
    with patch.object(agent.client.models, 'generate_content') as mock_gen:
        mock_gen.return_value.candidates = [
            type('obj', (object,), {
                'content': type('obj', (object,), {
                    'parts': [
                        type('obj', (object,), {'text': "Test caption", 'inline_data': None}),
                    ]
                })()
            })
        ]
        text, image = agent.generate_image_response("sunset")
        assert text == "Test caption"
        assert image is None
