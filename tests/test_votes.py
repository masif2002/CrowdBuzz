def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post('/vote/', json={
        "post_id": test_posts[2].id,
        "dir": 1
    })
    assert res.status_code == 201
    
def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={
        "post_id": test_posts[2].id,
        "dir": 1
    })
    assert res.status_code == 403

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={
        "post_id": test_posts[2].id,
        "dir": 0
    })
    assert res.status_code == 201

def test_delete_non_exist_vote(authorized_client, test_posts):
    res = authorized_client.post('/vote/', json={
        "post_id": test_posts[2].id,
        "dir": 0
    })
    assert res.status_code == 403

def test_vote_on_non_exist_post(authorized_client, test_posts):
    res = authorized_client.post('/vote/', json={
        "post_id": "999999",
        "dir": 1
    })
    assert res.status_code == 404

def test_unauthorized_vote_on_post(client, test_posts):
    res = client.post('/vote/', json={
        "post_id": test_posts[2].id,
        "dir": 1
    })
    assert res.status_code == 401