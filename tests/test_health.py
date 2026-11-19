def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_health_response_not_empty(client):
    response = client.get("/health")

    assert response.json() != {}
