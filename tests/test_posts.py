from fastapi import status
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')

    # Checking to see if we got our response as the way we expected
    def validate(posts):
        return schemas.PostOut(**posts)
    posts = map(validate, res.json())
     
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/89484')
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id

def test_create_post(authorized_client, test_user):
    post = {
            "title": "CHacHcaCha There",
            "content": "flask is fun",
            "published": True,
            "user_id": test_user['id']
    }
    res = authorized_client.post('/posts/', json=post)
    response = schemas.Post(**res.json())
    assert res.status_code == 201
    assert response.content == "flask is fun"

def test_create_post_default_published(authorized_client):
    post = {
            "title": "CHacHcaCha There",
            "content": "flask is fun"
    }
    res = authorized_client.post('/posts/', json=post)
    response = schemas.Post(**res.json())

    assert res.status_code == 201
    assert response.published == True

def test_unauthorized_user_create_post(client):
    post = {
            "title": "CHacHcaCha There",
            "content": "flask is fun"
    }
    res = client.post('/posts/', json=post)
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')

    assert res.status_code == 204

def test_delete_non_exist_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/9999999999')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[2].id}')
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json={
        "title": "Updated title",
        "content": "Updated content"
    })
    assert res.status_code == 200
    assert res.json()['title'] == "Updated title"
    assert res.json()['content'] == "Updated content"

def test_update_other_user_post(authorized_client, test_posts):
    res = authorized_client.put(f'/posts/{test_posts[2].id}', json={
        "title": "Updated title",
        "content": "Updated content"
    })
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}', json={
        "title": "Updated title",
        "content": "Updated content"
    })
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_posts):
    res = authorized_client.put(f'/posts/9999999999', json={
        "title": "Updated title",
        "content": "Updated content"
    })
    assert res.status_code == 404