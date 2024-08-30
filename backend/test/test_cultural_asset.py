"""
All e2e_tests for cultural asset endpoints.
"""


def test_cultural_asset_get_by_id(with_client):
    """
    Tests the get by id endpoint for cultural assets.
    """

    client = with_client
