import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.deps import get_current_user
from app.models import User
from app.security import create_access_token


class FakeQuery:
    def __init__(self, user):
        self.user = user

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.user


class FakeDB:
    def __init__(self, user=None):
        self.user = user

    def query(self, model):
        return FakeQuery(self.user)


def _bearer(token):
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_get_current_user_returns_user_for_valid_token():
    user = User(id=1, email="user@example.com", password="hashed")
    token = create_access_token(subject=user.email)

    result = get_current_user(credentials=_bearer(token), db=FakeDB(user))

    assert result.email == "user@example.com"


def test_get_current_user_raises_401_when_token_missing():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials=None, db=FakeDB(None))

    assert exc_info.value.status_code == 401


def test_get_current_user_raises_401_when_token_invalid():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials=_bearer("not-a-valid-token"), db=FakeDB(None))

    assert exc_info.value.status_code == 401


def test_get_current_user_raises_401_when_user_not_found():
    token = create_access_token(subject="ghost@example.com")

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials=_bearer(token), db=FakeDB(None))

    assert exc_info.value.status_code == 401
