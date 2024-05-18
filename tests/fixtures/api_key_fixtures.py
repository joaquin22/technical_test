import pytest
from rest_framework_api_key.models import APIKey


@pytest.fixture
def api_key() -> str:
    _, key = APIKey.objects.create_key(name="my-remote-service")

    return key
