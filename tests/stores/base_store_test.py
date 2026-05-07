import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, call
from models.user import User
from stores.base_store import BaseStore


@pytest.fixture
def store():
    return BaseStore()

def test_commit_success(mocker: MockerFixture, store: BaseStore):
    # given mock db session
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    commit: MagicMock = mock_session.commit

    # when commit called
    store.commit()

    # then commit should be only thing called during session
    assert mock_session.mock_calls == [call.commit()]
    commit.assert_called_once()

def test_add(mocker: MockerFixture, store: BaseStore):
    # given mock db session
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    add: MagicMock = mock_session.add
    commit: MagicMock = mock_session.commit
    
    # given somthing to add, User as an example
    expected_user = User()

    # when add called
    store.add(x=expected_user)

    # then only calls should be add(expected) and commit
    assert mock_session.mock_calls == [call.add(instance=expected_user), call.commit()]
    add.assert_called_once_with(instance=expected_user)
    commit.assert_called_once()
