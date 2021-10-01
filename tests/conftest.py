from tests.data import add_products, add_users
import pytest
from src import create_app, db
from config import Config, ConfigNames


@pytest.fixture(autouse=True, scope='session')
def setup_db():
    app = create_app(ConfigNames.TESTING)

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_users()
            add_products()
        yield client


@pytest.fixture
def client():
    app = create_app(ConfigNames.TESTING)

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client
