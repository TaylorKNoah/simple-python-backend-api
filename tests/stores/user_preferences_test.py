import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, call
from app import create_app
from models.user_preference import UserPreference
from stores.auth_store import AuthStore
from stores.user_preference_store import UserPreferenceStore

@pytest.fixture
def pref_store():
    return UserPreferenceStore()

@pytest.fixture
def user_store():
    return AuthStore()

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    with app.app_context():
        yield

def test_create_user_preference_success(mocker: MockerFixture, pref_store: UserPreferenceStore, user_store: AuthStore):
    # given mock db session
    mock_session: MagicMock = mocker.patch("startup.extensions.db.session")
    add: MagicMock = mock_session.add
    commit: MagicMock = mock_session.commit

    # given user pref
    user_pref = UserPreference()

    # when create_user_preference called
    pref_store.create_user_preference(user_pref)

    # then mock calls match expected
    assert mock_session.mock_calls == [call.add(instance=user_pref), call.commit()]
    add.assert_called_once()
    commit.assert_called_once()

def test_get_user_preference_success(mocker: MockerFixture, pref_store: UserPreferenceStore):
    # given expected user preference
    expected_user_pref = UserPreference(
        user_id=0,
        display_name="test name",
        email="test email",
        country="test country"
    )

    # given expected query calls
    expected_query_calls = [call(user_id=expected_user_pref.user_id), call().first()]
    
    # given query returns expected value
    mock_query: MagicMock = mocker.patch("stores.user_preference_store.UserPreference.query")
    filter_by: MagicMock = mock_query.filter_by
    filter_by.return_value.first.return_value = expected_user_pref

    # when store get_user_preference called
    actual_user_pref = pref_store.get_user_preference(expected_user_pref.user_id)

    # then query calls and returned user preference match expected
    filter_by.assert_called_once_with(user_id=expected_user_pref.user_id)
    assert filter_by.mock_calls == expected_query_calls
    assert actual_user_pref == expected_user_pref
