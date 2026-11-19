def test_search_endpoint(client):
    response = client.get("/search", params={"q": "Pune"})
    assert response.status_code == 200


def test_search_returns_valid_response(client):
    response = client.get("/search", params={"q": "Mumbai"})
    assert response.status_code == 200
    assert isinstance(response.json(), (list, dict))
