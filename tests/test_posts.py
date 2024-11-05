from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_post():
    # First create a user
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "postuser@example.com",
            "username": "postuser",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    # Create post
    response = client.post(
        "/api/v1/posts/",
        json={
            "title": "Test Post",
            "content": "This is a test post content"
        },
        params={"user_id": user_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post content"
    assert data["user_id"] == user_id
    assert "created_at" in data
    assert "updated_at" in data

def test_read_post():
    # Create a user and post first
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "readpost@example.com",
            "username": "readpost",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    post_response = client.post(
        "/api/v1/posts/",
        json={
            "title": "Read Test Post",
            "content": "This is a test post for reading"
        },
        params={"user_id": user_id}
    )
    post_id = post_response.json()["id"]
    
    # Read the post
    response = client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read Test Post"
    assert data["content"] == "This is a test post for reading"

def test_update_post():
    # Create a user and post first
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "updatepost@example.com",
            "username": "updatepost",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    post_response = client.post(
        "/api/v1/posts/",
        json={
            "title": "Update Test Post",
            "content": "This is a test post for updating"
        },
        params={"user_id": user_id}
    )
    post_id = post_response.json()["id"]
    
    # Update the post
    response = client.put(
        f"/api/v1/posts/{post_id}",
        json={
            "title": "Updated Post Title",
            "content": "This is the updated content"
        },
        params={"user_id": user_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Post Title"
    assert data["content"] == "This is the updated content"

def test_delete_post():
    # Create a user and post first
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "deletepost@example.com",
            "username": "deletepost",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    post_response = client.post(
        "/api/v1/posts/",
        json={
            "title": "Delete Test Post",
            "content": "This is a test post for deleting"
        },
        params={"user_id": user_id}
    )
    post_id = post_response.json()["id"]
    
    # Delete the post
    response = client.delete(
        f"/api/v1/posts/{post_id}",
        params={"user_id": user_id}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify post is deleted
    get_response = client.get(f"/api/v1/posts/{post_id}")
    assert get_response.status_code == 404

def test_read_user_posts():
    # Create a user
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "userposts@example.com",
            "username": "userposts",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    # Create multiple posts
    post_titles = ["First Post", "Second Post", "Third Post"]
    for title in post_titles:
        client.post(
            "/api/v1/posts/",
            json={
                "title": title,
                "content": f"Content for {title}"
            },
            params={"user_id": user_id}
        )
    
    # Get user's posts
    response = client.get(f"/api/v1/posts/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(post["user_id"] == user_id for post in data)
    assert all(post["title"] in post_titles for post in data)

def test_unauthorized_update():
    # Create two users
    user1_response = client.post(
        "/api/v1/users/",
        json={
            "email": "user1@example.com",
            "username": "user1",
            "password": "testpass123"
        }
    )
    user1_id = user1_response.json()["id"]
    
    user2_response = client.post(
        "/api/v1/users/",
        json={
            "email": "user2@example.com",
            "username": "user2",
            "password": "testpass123"
        }
    )
    user2_id = user2_response.json()["id"]
    
    # User1 creates a post
    post_response = client.post(
        "/api/v1/posts/",
        json={
            "title": "User1's Post",
            "content": "This is user1's post"
        },
        params={"user_id": user1_id}
    )
    post_id = post_response.json()["id"]
    
    # User2 tries to update User1's post
    response = client.put(
        f"/api/v1/posts/{post_id}",
        json={
            "title": "Unauthorized Update",
            "content": "This should not work"
        },
        params={"user_id": user2_id}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found or not authorized"
