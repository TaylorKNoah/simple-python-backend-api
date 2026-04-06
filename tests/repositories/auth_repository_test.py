import pytest
from unittest.mock import MagicMock
from models.user import User
from repositories.auth_repository import AuthRepository
from request_models.register_request import RegisterRequest
from stores.auth_store import AuthStore

@pytest.fixture
def mock_store():
    return MagicMock(spec=AuthStore)

@pytest.fixture
def repo(mock_store: MagicMock):
    return AuthRepository(auth_store=mock_store)

def test_register_user_success(repo: AuthRepository, mock_store: MagicMock):
    mock_store.get_user_by_name.return_value = None
    mock_store.create_user.return_value = MagicMock(spec=User)

    repo.register_user(RegisterRequest(name="test-name", password="test-password"))

    mock_store.get_user_by_name.assert_called_once_with("test-name")
    mock_store.create_user.assert_called_once()


def test_register_user_duplicate(repo: AuthRepository, mock_store: MagicMock):
    mock_store.get_user_by_name.return_value = MagicMock(spec=User)

    with pytest.raises(ValueError, match="already taken"):
        repo.register_user(RegisterRequest(name="test-name", password="test-password"))

    mock_store.create_user.assert_not_called()


def test_register_user_hashes_password(repo: AuthRepository, mock_store: MagicMock):
    mock_store.get_user_by_name.return_value = None
    mock_store.create_user.return_value = MagicMock(spec=User)

    repo.register_user(RegisterRequest(name="test-name", password="test-password"))

    _, kwargs = mock_store.create_user.call_args
    assert kwargs["password_hash"] != "test-password"