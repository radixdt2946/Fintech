def test_access(client):
    response = client.get("/")
    assert (response.status_code == 200)
