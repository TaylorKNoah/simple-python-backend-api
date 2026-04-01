import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
from stores.base_store import BaseStore


@pytest.fixture
def store():
    return BaseStore()


def test_commit_success(mocker: MockerFixture, store: BaseStore):
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    commit: MagicMock = mock_session.commit

    store._commit()

    commit.assert_called_once()


def test_commit_sqlalchemy_error(mocker: MockerFixture, store: BaseStore):
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    rollback: MagicMock = mock_session.rollback
    mock_session.commit.side_effect = SQLAlchemyError()

    with pytest.raises(SQLAlchemyError):
        store._commit()

    rollback.assert_called_once()


def test_commit_integrity_error(mocker: MockerFixture, store: BaseStore):
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    rollback: MagicMock = mock_session.rollback
    mock_session.commit.side_effect = SQLAlchemyError("unique constraint violated")

    with pytest.raises(SQLAlchemyError):
        store._commit()

    rollback.assert_called_once()