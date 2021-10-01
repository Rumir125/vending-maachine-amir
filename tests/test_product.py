from http import HTTPStatus
from tests.test_auth import get_token_for_user
from flask import json
from flask.testing import FlaskClient


def create(client: FlaskClient, amount_available, cost, product_name, seller_id, token):
    return client.post('/products', json=dict(
        amount_available=amount_available,
        cost=cost,
        product_name=product_name,
    ), follow_redirects=True, headers={'Authorization': token})


def get_all(client: FlaskClient):
    return client.get('/products')


def get(client: FlaskClient, product_id):
    return client.get(f'/products/{product_id}')


def delete(client: FlaskClient, product_id, token):
    return client.delete(f'/products/{product_id}', headers={'Authorization': token})


def update(client: FlaskClient, id, product, token):
    return client.put(f'/products/{id}', json=product, headers={'Authorization': token})


def test_create_unauthorized(client: FlaskClient):
    res = create(client, 50, 50, 'test', 1, "")
    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_create_wrong_role(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    res = create(client, 50, 50, 'test', 1, token)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_create_success(client: FlaskClient):
    token = get_token_for_user(client, 'seller')
    res = create(client, 50, 50, 'test', 1, token)
    assert res.status_code == HTTPStatus.CREATED


def test_get_all(client: FlaskClient):
    res = get_all(client)
    assert res.status_code == HTTPStatus.OK


def test_get_product_ok(client: FlaskClient):
    res = get(client, 1)
    assert res.status_code == HTTPStatus.OK


def test_get_product_not_found(client: FlaskClient):
    res = get(client, 99999)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_delete_unauthorized(client: FlaskClient):
    res = delete(client, 3, '')
    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_forbidden(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    res = delete(client, 3, token)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_delete_not_found(client: FlaskClient):
    token = get_token_for_user(client, 'seller')
    res = delete(client, 99999, token)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_delete_ok(client: FlaskClient):
    token = get_token_for_user(client, 'seller')
    res = delete(client, 3, token)
    assert res.status_code == HTTPStatus.OK

    res = get(client, 3)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_update_unauthorized(client: FlaskClient):
    res = update(client, 1, {
        "amount_available": 50,
        "cost": 150,
        "product_name": "new_name"
    }, '')

    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_update_forbidden(client: FlaskClient):
    token = get_token_for_user(client, 'buyer')
    res = update(client, 1, {
        "amount_available": 50,
        "cost": 150,
        "product_name": "new_name"
    }, token)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_update_not_found(client: FlaskClient):
    token = get_token_for_user(client, 'seller')
    res = update(client, 99999, {
        "amount_available": 50,
        "cost": 150,
        "product_name": "new_name"
    }, token)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_update_ok(client: FlaskClient):
    token = get_token_for_user(client, 'seller')
    res = update(client, 1, {
        "amount_available": 50,
        "cost": 150,
        "product_name": "new_name"
    }, token)
    assert res.status_code == HTTPStatus.OK
    data = json.loads(res.data)
    assert data['amount_available'] == 50
    assert data['cost'] == 150
    assert data['product_name'] == 'new_name'
