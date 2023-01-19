import pytest


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = "test_user",
    password = "test_password"

    django_user_model.objects.create_user(username=username, password=password, role="moderator")

    response = client.post("/user/token/", {"username": username, "password": password}, format='json')

    return response.data
