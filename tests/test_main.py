import pytest
from main import chat_response

@pytest.mark.asyncio
async def test_chat_response_yields_text():
    prompt = "test"
    response = chat_response(prompt)
    results = []
    async for chunk in response:
        results.append(chunk)
    assert any(isinstance(r, str) for r in results)
