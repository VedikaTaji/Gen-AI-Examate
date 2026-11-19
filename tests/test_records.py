def test_records_endpoint(client):
    response = client.get("/records")
    assert response.status_code == 200
    assert isinstance(response.json(), (list, dict))


def test_records_response_not_empty(client):
    response = client.get("/records")
    assert response.status_code == 200
    assert len(response.json()) > 0
