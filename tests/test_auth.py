from http import HTTPStatus
from flask.testing import FlaskClient
from flask import json


def login(client: FlaskClient, username, password):
    return client.post(f'/login', json=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def get_token_for_user(client: FlaskClient, role):
    username = 'user1' if role == 'seller' else 'user2'
    res = login(client, username, 'test')
    return json.loads(res.data)['auth_token']


def test_login_forbidden(client: FlaskClient):
    res = login(client, 'no_data', 'no_data')
    assert res.status_code == HTTPStatus.FORBIDDEN
