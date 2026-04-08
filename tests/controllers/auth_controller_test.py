from flask_jwt_extended import create_access_token
import pytest
from unittest.mock import MagicMock, patch
from flask.testing import FlaskClient
from werkzeug.security import generate_password_hash

from app import create_app
from models.user import User
from response_models.login_response import LoginResponse
from response_models.register_response import RegisterResponse


@pytest.fixture(scope='function')
def test_client():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        with app.test_client() as testing_client:
            yield testing_client

#################################################################################################################
###################  /register                                                ###################################
#################################################################################################################

def test_regitser_returns_201(test_client: FlaskClient):
    new_user = User(id=1, name="test-user")

    with patch('controllers.auth_controller.auth_repository_instance') as mock_repo:
        mock_repo.register_user.return_value = new_user

        response = test_client.post(
            "auth/register",
            json={
                "name": "test-user",
                "password": "1234"
            }
        )

        data = response.get_json()

        assert response.status_code == 201
        assert data['id'] == new_user.id
        assert data['name'] == new_user.name

@pytest.mark.parametrize(
    "payload, expected_status, expected_error_type, expected_error_param",
    [
        (None, 422, 'model_type', []), # no body
        ({}, 422, 'missing', ['name']), # empty body
        ({"name": "test-name"}, 422, 'missing', ['password']), # missing password
        ({"password": "test-password"}, 422, 'missing', ['name']), # missing name
        ({"name": "", "password": "test-password"}, 422, 'string_too_short', ['name']), # name too short
        ({"name": "0123456789012345678901234567890123", "password": "test-password"}, 422, 'string_too_long', ['name']), # name too long
        ({"name": "test-name", "password": "123"}, 422, 'string_too_short', ['password']), # password too short
        ({"name": "test-name", "password": "0123456789012345678901234567890123"}, 422, 'string_too_long', ['password']), # password too long
    ]
)
def test_register_fails_validation_returns_422(test_client: FlaskClient, payload, expected_status, expected_error_type, expected_error_param):
    response = test_client.post(
        "auth/register",
        json=payload
    )

    error = response.get_json()[0]

    assert response.status_code == expected_status
    assert error['type'] == expected_error_type
    assert error['loc'] == expected_error_param

def test_register_user_exists_returns_409(test_client: FlaskClient):
    expected_error_message = "Username 'test-user' is already taken."

    with patch('controllers.auth_controller.auth_repository_instance') as mock_repo:
        mock_repo.register_user.side_effect = ValueError(expected_error_message)

        response = test_client.post(
            "auth/register",
            json={
                'name': 'test-user',
                'password': 'test-password'
            }
        )

        data = response.get_json()

        assert response.status_code == 409
        assert data['ErrorMessage'] == expected_error_message

def test_register_exception_returns_500(test_client: FlaskClient):
    expected_error_message = "Something happened..."

    with patch('controllers.auth_controller.auth_repository_instance') as mock_repo:
        mock_repo.register_user.side_effect = Exception(expected_error_message)

        response = test_client.post(
            "auth/register",
            json={
                'name': 'test-user',
                'password': 'test-password'
            }
        )

        data = response.get_json()

        assert response.status_code == 500
        assert data['ErrorMessage'] == expected_error_message

#################################################################################################################
###################  /login                                                   ###################################
#################################################################################################################

def test_login_user_returns_jwt_token_on_201(test_client: FlaskClient):
    with patch('controllers.auth_controller.auth_repository_instance') as mock_repo:
        mock_repo.login_user.return_value = User(id=1, name="test-user")

        response = test_client.post(
            'auth/login',
            json={
                "name": "test-user",
                "password": "test-password"
            }
        )

        data = response.get_json()
        has_token = "jwt_token" in data

        assert response.status_code == 201
        assert has_token == True
        assert len(data) == 1

def test_login_user_value_error_returns_401(test_client: FlaskClient):
    with patch('controllers.auth_controller.auth_repository_instance') as mock_repo:
        mock_repo.login_user.side_effect = ValueError("Invalid Credentials")

        response = test_client.post(
            'auth/login',
            json={
                "name": "test-name",
                "password": "test-password"
            }
        )

        data = response.get_json()

        assert response.status_code == 401
        assert data['ErrorMessage'] == "Invalid Credentials"

@pytest.mark.parametrize(
    "payload, expected_status, expected_error_type, expected_error_param",
    [
        (None, 422, 'model_type', []), # no body
        ({}, 422, 'missing', ['name']), # empty body
        ({"name": "test-name"}, 422, 'missing', ['password']), # missing password
        ({"password": "test-password"}, 422, 'missing', ['name']), # missing name
        ({"name": "", "password": "test-password"}, 422, 'string_too_short', ['name']), # name too short
        ({"name": "0123456789012345678901234567890123", "password": "test-password"}, 422, 'string_too_long', ['name']), # name too long
        ({"name": "test-name", "password": "123"}, 422, 'string_too_short', ['password']), # password too short
        ({"name": "test-name", "password": "0123456789012345678901234567890123"}, 422, 'string_too_long', ['password']), # password too long
    ]
)
def test_login_fails_validation_returns_422(test_client: FlaskClient, payload, expected_status, expected_error_type, expected_error_param):
    response = test_client.post(
        "auth/login",
        json=payload
    )

    error = response.get_json()[0]

    assert response.status_code == expected_status
    assert error['type'] == expected_error_type
    assert error['loc'] == expected_error_param

def test_login_user_exception_returns_500(test_client: FlaskClient):
    with patch('controllers.auth_controller.auth_repository_instance') as mock_repo:
        mock_repo.login_user.side_effect = Exception("something happened")

        response = test_client.post(
            'auth/login',
            json={
                "name": "test-name",
                "password": "test-password"
            }
        )

        data = response.get_json()

        assert response.status_code == 500
        assert data['ErrorMessage'] == "something happened"