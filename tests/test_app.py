import pytest
from unittest.mock import patch, MagicMock
import app

@pytest.mark.asyncio
async def test_app_runs(monkeypatch):
    # Patch chat_response to avoid calling actual API
    async def mock_chat_response(prompt):
        yield "Mock response text"

    monkeypatch.setattr(app, "chat_response", mock_chat_response)

    # We simulate that the session state exists to avoid full UI rendering
    app.st = MagicMock()
    app.st.session_state = {"messages": []}
    app.st.chat_input.return_value = "A cat flying in space"

    # Mock methods to avoid full Streamlit UI dependency
    app.st.chat_message = MagicMock()
    app.st.image = MagicMock()
    app.st.write = MagicMock()
    app.st.spinner = MagicMock()
    app.st.warning = MagicMock()
    app.st.markdown = MagicMock()
    app.st.empty = MagicMock(return_value=MagicMock())

    # Now run the async function
    await app.run_chat()

    # Validate that the prompt was passed
    assert app.st.chat_input.called
