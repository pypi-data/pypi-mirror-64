def test_requests(client):
    response = client.post("/test/requests/", format="json")

    assert response.status_code == 400

    response_data = response.json()
    assert response_data["code"] == "InvalidToken"
    assert response_data["description"] == "Invalid token."
