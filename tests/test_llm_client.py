# tests/test_llm_client.py

import pytest
import llm_client
from unittest.mock import patch, MagicMock

def test_successful_llm_call():
    prompt = "Hello?"
    mock_response_data = {"response": "Hi there!"}

    with patch("llm_client.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        mock_post.return_value.json.return_value = mock_response_data

        result = llm_client.call_local_llm(prompt)
        assert result == "Hi there!"
        mock_post.assert_called_once()

def test_failed_llm_call():
    with patch("llm_client.requests.post") as mock_post:
        mock_post.side_effect = Exception("Connection error")

        result = llm_client.call_local_llm("Hi")
        assert result.startswith("[ERROR]")
        assert "Connection error" in result
