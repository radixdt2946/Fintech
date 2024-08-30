import pytest
from app import create_app
# from flaskr import flaskr


@pytest.fixture
def client():
    client = create_app()
    client.config.update({
        "TESTING": True,
    })

    yield client.test_client()


    # with app.test_client() as client:
    #     yield client

# @pytest.fixture()
# def client(client):
#     return client.test_backtest()


# @pytest.fixture()
# def runner(client):
#     return client.test_cli_runner()