import pytest
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings as s
from app.database import Base, get_db
from app import models
from app.utils import hash_password
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{s.database_username}:{s.database_password}@{s.database_hostname}/{s.database_name}_tests"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Session for testing

Base.metadata.create_all(bind=engine) # Creates all the tables for testing session


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
        
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(session):
    new_user = {'email': 'testing@gmail.com', 'password': 'password123'}
    
    session.add(models.User(email=new_user['email'], password=hash_password(new_user['password'])))
    session.commit()

    user_id = session.query(models.User).filter(models.User.email == new_user['email']).first().id
    new_user['id'] = user_id

    return new_user

@pytest.fixture
def test_user2(session):
    new_user = {'email': 'testing2@gmail.com', 'password': 'password123'}
    
    session.add(models.User(email=new_user['email'], password=hash_password(new_user['password'])))
    session.commit()

    user_id = session.query(models.User).filter(models.User.email == new_user['email']).first().id
    new_user['id'] = user_id

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(token, client):
    client.headers= {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    data = [
        {
            "title": "Hey There",
            "content": "Learning is fun",
            "published": True,
            "user_id": test_user['id']
        },
        {
            "title": "Hello There",
            "content": "API is fun",
            "published": True,
            "user_id": test_user['id']
        },
        {
            "title": "Hows There",
            "content": "fastaPI is fun",
            "published": True,
            "user_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, data))

    session.add_all(posts)    
    session.commit()

    posts = session.query(models.Post).all()
    return posts

@pytest.fixture
def test_vote(session, test_user, test_posts):
    vote = models.Vote(user_id=test_user['id'], post_id=test_posts[2].id)
    session.add(vote)
    session.commit()

    return