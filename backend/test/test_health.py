"""
    All e2e_tests pertinent to health pipeline.
"""


def test_health(with_client):
    """
    Tests the health endpoint.
    """
    client = with_client

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
