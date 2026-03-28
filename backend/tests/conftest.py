# test
from unittest.mock import MagicMock
import pytest

# fastapi
from fastapi.testclient import TestClient

# app
from app.main import app


def gql(query: str) -> dict:
    return {
        "query": "{ " + query + " }"
    }


@pytest.fixture()
def client():

    # Http client to tests without up the fast api server
    return TestClient(
        app,
        raise_server_exceptions=False
    )


@pytest.fixture()
def mock_db():
    session = MagicMock()

    session.query.return_value = session
    session.filter.return_value = session
    session.offset.return_value = session
    session.limit.return_value = session
    session.count.return_value = 0
    session.all.return_value = []
    session.first.return_value = None
    
    return session
