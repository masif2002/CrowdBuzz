import pytest
from app import schemas
from jose import jwt
from app.config import settings



def test_root(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json().get('message') == 'Hello World!!'

def test_create_user(client):
    res = client.post('/users/', json={"email": "asif@facebook.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "asif@facebook.com"

def test_login(test_user, client):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})

    # Verifying if we got the response as exxpected
    response_data = schemas.Token(**res.json())

    # verifying token
    payload = jwt.decode(response_data.token, f"{settings.secret_key}", algorithms=[f"{settings.algorithm}"]) 
    id = payload.get('user_id')

    assert id == test_user['id']
    assert response_data.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, response", [
    ("testing@gmail.com", "jsfbjdshbfjhb", 403),
    ("dsjsdkf@okdokie.com", "password123", 403),
    ("jdbfhbsf@jhbf.com", "ewksjdfhjdb", 403),
    (None, "password123", 422),
    ("testing@gmail.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, response):
    res = client.post('/login', data={"username": email, "password": password})

    assert res.status_code == response