import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
from stores.auth_store import AuthStore

@pytest.fixture
def store():
    return AuthStore()

def test_create_user_success(mocker: MockerFixture, store: AuthStore):
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    add: MagicMock = mock_session.add
    commit: MagicMock = mock_session.commit

    user = store.create_user(name="alice", password_hash="hashed")

    add.assert_called_once()
    commit.assert_called_once()
    assert user.name == "alice"
    assert user.password_hash == "hashed"


def test_create_user_integrity_error(mocker: MockerFixture, store: AuthStore):
    mocker.patch("startup.extensions.db.session")
    mocker.patch.object(store, "_commit", side_effect=ValueError("integrity error"))

    with pytest.raises(ValueError, match="integrity error"):
        store.create_user(name="alice", password_hash="hashed")


def test_create_user_sqlalchemy_error(mocker: MockerFixture, store: AuthStore):
    mocker.patch("startup.extensions.db.session")
    mocker.patch.object(store, "_commit", side_effect=SQLAlchemyError())

    with pytest.raises(SQLAlchemyError):
        store.create_user(name="alice", password_hash="hashed")