from unittest.mock import patch


def test_ask_with_fake_llm(client):
    fake_response = {
        "question": "What is AQI?",
        "answer": "AQI measures air quality.",
        "citations": [],
        "confidence": "high",
        "retrieved_chunks": 1,
    }

    with patch("app.main.answer_with_rag", return_value=fake_response) as mock_rag:
        response = client.post("/ask", json={"question": "What is AQI?"})

    assert response.status_code == 200
    assert response.json() == fake_response

    mock_rag.assert_called_once_with(question="What is AQI?", top_k=5)
