import pytest


@pytest.mark.django_db
def test_ad_create(client, access_token, user, category):
    data = {
        "id": 11,
        "author": user.pk,
        "category": category.pk,
        "name": "Слэб из стола",
        "price": 100500,
        "description": "",
    }

    expected_data = {
        "id": 1,
        "author": user.pk,
        "category": category.pk,
        "name": "Слэб из стола",
        "price": 100500,
        "description": "",
        "is_published": False,
        "image": None
    }

    response = client.post("/ad/", data, HTTP_AUTHORIZATION="Bearer " + access_token)

    assert response.status_code == 201
    assert response.data == expected_data
