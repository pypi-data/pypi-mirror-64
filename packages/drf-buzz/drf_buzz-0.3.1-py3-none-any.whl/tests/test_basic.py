def test_basic_validation_error(client):
    response = client.post("/test/", format="json")

    assert response.status_code == 400

    response_data = response.json()
    assert response_data["code"] == "ValidationError"
    assert response_data["description"] == "Invalid input."


def test_basic_buzz(client):
    response = client.post("/test/buzz/", format="json")

    assert response.status_code == 500

    response_data = response.json()
    assert response_data["code"] == "DRFBuzz"
    assert response_data["description"] == "basic error"


def test_basic_exception(client):
    response = client.post("/test/exception/", format="json")

    assert response.status_code == 500

    response_data = response.json()
    assert response_data["code"] == "APIException"
    assert response_data["description"] == "Internal error"
