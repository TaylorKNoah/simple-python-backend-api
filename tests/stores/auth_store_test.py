import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
from app import create_app
from models.user import User
from stores.auth_store import AuthStore

@pytest.fixture
def store():
    return AuthStore()

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    with app.app_context():
        yield

def test_create_user_success(mocker: MockerFixture, store: AuthStore):
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    add: MagicMock = mock_session.add
    commit: MagicMock = mock_session.commit

    user = store.create_user(name="test-name", password_hash="test-hash")

    add.assert_called_once()
    commit.assert_called_once()
    assert user.name == "test-name"
    assert user.password_hash == "test-hash"


def test_create_user_integrity_error(mocker: MockerFixture, store: AuthStore):
    mocker.patch("startup.extensions.db.session")
    mocker.patch.object(store, "_commit", side_effect=ValueError("integrity error"))

    with pytest.raises(ValueError, match="integrity error"):
        store.create_user(name="test-name", password_hash="test-hash")


def test_create_user_sqlalchemy_error(mocker: MockerFixture, store: AuthStore):
    mocker.patch("startup.extensions.db.session")
    mocker.patch.object(store, "_commit", side_effect=SQLAlchemyError())

    with pytest.raises(SQLAlchemyError):
        store.create_user(name="test-name", password_hash="test-hash")

def test_get_user_by_name_success(mocker: MockerFixture, store: AuthStore):
    mock_query: MagicMock = mocker.patch("stores.auth_store.User.query")
    mock_user = MagicMock(spec=User)
    filter_by: MagicMock = mock_query.filter_by
    first: MagicMock = filter_by.return_value.first
    first.return_value = mock_user

    result = store.get_user_by_name("test-name")

    filter_by.assert_called_once_with(name="test-name")
    first.assert_called_once()
    assert result == mock_user

def test_get_user_by_name_not_found(mocker: MockerFixture, store: AuthStore):
    mock_query: MagicMock = mocker.patch("stores.auth_store.User.query")
    filter_by: MagicMock = mock_query.filter_by
    first: MagicMock = filter_by.return_value.first
    first.return_value = None

    result = store.get_user_by_name("test-name")

    filter_by.assert_called_once_with(name="test-name")
    assert result is None