from jose import jwt

from app.security import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_does_not_return_plain_text():
    hashed = hash_password("mysecretpassword")

    assert hashed != "mysecretpassword"


def test_hash_password_produces_bcrypt_hash():
    hashed = hash_password("mysecretpassword")

    assert hashed.startswith("$2b$")


def test_verify_password_succeeds_for_correct_password():
    hashed = hash_password("mysecretpassword")

    assert verify_password("mysecretpassword", hashed) is True


def test_verify_password_fails_for_incorrect_password():
    hashed = hash_password("mysecretpassword")

    assert verify_password("wrongpassword", hashed) is False


def test_hash_password_generates_different_hashes_for_same_password():
    first = hash_password("mysecretpassword")
    second = hash_password("mysecretpassword")

    assert first != second


def test_create_access_token_contains_subject_and_expiration():
    token = create_access_token(subject="user@example.com")

    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

    assert payload["sub"] == "user@example.com"
    assert "exp" in payload


def test_create_access_token_is_decodable_only_with_correct_secret():
    token = create_access_token(subject="user@example.com")

    try:
        jwt.decode(token, "wrong-secret", algorithms=[JWT_ALGORITHM])
        assert False, "expected decoding with wrong secret to fail"
    except jwt.JWTError:
        pass
