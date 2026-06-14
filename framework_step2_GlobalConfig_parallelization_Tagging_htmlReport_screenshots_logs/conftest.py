import pytest

@pytest.fixture(scope="session")
def user_credentials(request):
    print("executing user_credentials fixture from conftext.py")
    return request.param