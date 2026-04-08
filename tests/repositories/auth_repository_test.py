import pytest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash
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

#################################################################################################################
###################  register_user                                            ###################################
#################################################################################################################

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

#################################################################################################################
###################  login_user                                               ###################################
#################################################################################################################

def test_login_user_should_return_user_on_success(repo: AuthRepository, mock_store: MagicMock):
    expectedPassword = "test-password"
    expectedPasswordHash = generate_password_hash(expectedPassword)
    expectedUser: User = User(id=1, name="test-name", password_hash=expectedPasswordHash)
   
    mock_store.get_user_by_name.return_value = expectedUser

    actualUser = repo.login_user(expectedUser.name, expectedPassword)

    assert actualUser == expectedUser

def test_login_user_raises_value_error_when_user_not_found(repo: AuthRepository, mock_store: MagicMock):
    mock_store.get_user_by_name.return_value = None

    with pytest.raises(ValueError, match="Invalid Credentials"):
        repo.login_user(name="test-name", password="test-password")

def test_login_user_raises_value_error_when_user_not_found(repo: AuthRepository, mock_store: MagicMock):
    wrong_password = generate_password_hash("wrong-passwrod")
    expectedUser: User = User(id=1, name="test-name", password_hash=generate_password_hash("test-password"))
    mock_store.get_user_by_name.return_value = expectedUser

    with pytest.raises(ValueError, match="Invalid Credentials"):
        repo.login_user(name="test-name", password=wrong_password)