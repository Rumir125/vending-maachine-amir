from http import HTTPStatus
from src.models.user import User
from tests.test_auth import get_token_for_user

from flask import json
from flask.testing import FlaskClient
from src import jwt


def register(client: FlaskClient, username, password):
    return client.post('/users', json=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def get_all(client: FlaskClient):
    return client.get('/users')


def get(client: FlaskClient, user_id):
    return client.get(f'/users/{user_id}')


def delete(client: FlaskClient, user_id):
    return client.delete(f'/users/{user_id}')


def update(client: FlaskClient, id, user):
    return client.put(f'/users/{id}', json=user)


def reset_deposit(client: FlaskClient, token, user_id):
    return client.patch('/reset_deposit', json={"user_id": user_id }, headers={'Authorization': token})


def deposit(client: FlaskClient, deposit, token, user_id):
    return client.patch('/deposit', json={"deposit": deposit, "user_id": user_id}, headers={'Authorization': token})


def buy(client: FlaskClient, product_id, amount, token):
    return client.post('/buy', json={"product_id": product_id, "amount": amount}, headers={'Authorization': token})


def get_user_id_from_data(data):
    auth_token = data["auth_token"]
    payload = jwt.decode(auth_token)
    user_id = payload.user_id
    return user_id


def get_invalid_token(client):
    res = register(client, 'not_found_user', 'test')
    token = json.loads(res.data)['auth_token']

    user_id = get_user_id_from_data(json.loads(res.data))
    user = get(client, user_id)
    user = json.loads(user.data)

    delete(client, user_id)
    return token


def test_registration(client: FlaskClient):
    res = register(client, 'test', 'test')
    assert res.status_code == HTTPStatus.CREATED
    assert b'auth_token' in res.data

    user_id = get_user_id_from_data(json.loads(res.data))
    assert user_id is not None

    user = get(client, user_id)
    user = json.loads(user.data)
    user['deposit'] = 100
    update(client, user_id, {"deposit": user['deposit'], "username":user["username"]})
    user = get(client, user_id)
    user = json.loads(user.data)

    assert user['deposit'] == 100
    delete(client, user_id)


def test_password_hash(client: FlaskClient):
    password = 'test'
    user = User(password=password)
    assert user != user.password


def test_update_user_not_valid(client: FlaskClient):
    res = update(client, 99999, {})
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_doesnt_exist(client: FlaskClient):
    res = delete(client, 99999)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_registration_credentials_taken(client: FlaskClient):
    res = register(client, 'user1', 'password')
    assert res.status_code == HTTPStatus.CONFLICT


def test_registration_success(client: FlaskClient):
    res = register(client, 'username', 'password')
    assert res.status_code == HTTPStatus.CREATED
    assert b'auth_token' in res.data


def test_get_all(client: FlaskClient):
    res = get_all(client)
    assert res.status_code == HTTPStatus.OK


def test_get_user_ok(client: FlaskClient):
    res = get(client, 1)
    assert res.status_code == HTTPStatus.OK


def test_get_user_not_found(client: FlaskClient):
    res = get(client, 99999)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_ok(client: FlaskClient):
    res = delete(client, 3)
    assert res.status_code == HTTPStatus.OK


def test_delete_user_not_found(client: FlaskClient):
    res = delete(client, -1)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_update_user_ok(client: FlaskClient):
    res = update(client, 2, {'username': 'user2', 'password': 'test'})
    assert res.status_code == HTTPStatus.OK


def test_update_user_not_found(client: FlaskClient):
    res = update(client, -1, None)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_update_conflict(client: FlaskClient):
    res = update(client, 2, {'username': 'user1', 'password': 'test'})
    assert res.status_code == HTTPStatus.CONFLICT


def test_reset_deposit_ok(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    payload = jwt.decode(token)
    res = reset_deposit(client, token, payload.user_id)
    assert res.status_code == HTTPStatus.OK


def test_reset_deposit_user_not_found(client: FlaskClient):
    token = get_invalid_token(client)
    payload = jwt.decode(token)
    res = reset_deposit(client, token, payload.user_id)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_reset_deposit_unauthorized(client: FlaskClient):
    res = reset_deposit(client, None , 0)
    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_reset_deposit_not_valid_role(client: FlaskClient):
    token = get_token_for_user(client, 'seller')
    payload = jwt.decode(token)
    res = reset_deposit(client, token, payload.user_id)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_deposit_ok(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    payload = jwt.decode(token)
    res = deposit(client, 100, token, payload.user_id)
    assert res.status_code == HTTPStatus.OK


def test_deposit_user_not_found(client: FlaskClient):
    token = get_invalid_token(client)
    payload = jwt.decode(token)
    res = deposit(client, 0, token, payload.user_id)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_deposit_not_authorized(client: FlaskClient):
    res = deposit(client, 0, None, 0)
    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_deposit_not_valid_role(client: FlaskClient):
    token = get_token_for_user(client, 'seller')
    payload = jwt.decode(token)
    res = deposit(client, 0, token, payload.user_id)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_deposit_conflict(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    payload = jwt.decode(token)
    res = deposit(client, 33, token, payload.user_id)
    assert res.status_code == HTTPStatus.CONFLICT


def test_buy_ok(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    payload = jwt.decode(token)
    reset_deposit(client, token, payload.user_id)
    deposit(client, 100, token, payload.user_id)
    deposit(client, 50, token, payload.user_id)
    res = buy(client, 1, 1, token)
    assert res.status_code == HTTPStatus.OK
    data = json.loads(res.data)
    assert data['money_spent'] == 150
    # assert data['change'] == []


def test_buy_change_ok(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    payload = jwt.decode(token)
    reset_deposit(client, token, payload.user_id)
    for i in range(10):
        deposit(client, 100, token, payload.user_id)

    res = buy(client, 1, 1, token)
    assert res.status_code == HTTPStatus.OK
    data = json.loads(res.data)
    assert data['money_spent'] == 150
    total_coins_left = 850
    for change in data['change']:
        total_coins_left -= change['amount'] * change['coin']
    assert data['money_left'] == 850


def test_buy_product_not_found(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    res = buy(client, 999999, 1, token)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_buy_product_low_amount(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    res = buy(client, 1, 9999, token)
    assert res.status_code == HTTPStatus.CONFLICT


def test_buy_user_not_found(client: FlaskClient):
    token = get_invalid_token(client)
    res = buy(client, 1, 1, token)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_buy_user_not_enough_funds(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    payload = jwt.decode(token)
    reset_deposit(client, token, payload.user_id)
    res = buy(client, 1, 1, token)
    assert res.status_code == HTTPStatus.CONFLICT
