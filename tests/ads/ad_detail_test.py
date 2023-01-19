import pytest

from ads.serializers import AdSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ads_list(client, access_token):
    ad = AdFactory.create()

    response = client.get(f"/ad/{ad.pk}", HTTP_AUTHORIZATION="Bearer " + access_token)

    assert response.status_code == 200
    assert response.data == {
        "count": 5,
        "next": None,
        "previous": None,
        "results": AdSerializer(ad, many=True).data}