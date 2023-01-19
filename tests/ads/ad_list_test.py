import pytest

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ads_list(client, access_token):
    ad_list = AdFactory.create_batch(5)

    response = client.get("/ad/", HTTP_AUTHORIZATION="Bearer " + access_token)

    assert response.status_code == 200
    assert response.data == {
        "count": 5,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ad_list, many=True).data}

