import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, call
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

def test_create_user(mocker: MockerFixture, store: AuthStore):
    # given mock db session
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    add: MagicMock = mock_session.add
    commit: MagicMock = mock_session.commit

    # given user
    user = User(name="test_name", password_hash="test_hash")

    # when create_user called
    store.create_user(user)

    # then mock calls match expected
    assert mock_session.mock_calls == [call.add(instance=user), call.commit()]
    add.assert_called_once()
    commit.assert_called_once()

def test_get_user_by_name(mocker: MockerFixture, store: AuthStore):
    # given user
    user = User(name="test-name")

    # given query returns user
    mock_query: MagicMock = mocker.patch("stores.auth_store.User.query")
    filter_by: MagicMock = mock_query.filter_by
    first: MagicMock = filter_by.return_value.first
    first.return_value = user

    # when get_user_by_name called
    result = store.get_user_by_name("test-name")

    # then result matches user and mock calls match expected
    assert result == user
    assert mock_query.mock_calls == [call.filter_by(name='test-name'), call.filter_by().first()]
    filter_by.assert_called_once_with(name="test-name")
    first.assert_called_once()