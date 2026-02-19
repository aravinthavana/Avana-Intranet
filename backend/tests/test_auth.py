import pytest
import bcrypt
from database import db, AdminInfo

def test_check_auth_unauthorized(client):
    """Test accessing protected route without login"""
    response = client.get('/api/check-auth')
    assert response.status_code == 401

def test_login_flow(client, app):
    """Test full login flow: seed admin -> login -> check-auth -> logout"""
    
    # 1. Seed Admin
    password = "securepassword123"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    with app.app_context():
        admin = AdminInfo(password_hash=hashed)
        db.session.add(admin)
        db.session.commit()

    # 2. Login
    response = client.post('/api/login', json={'password': password})
    assert response.status_code == 200
    assert response.json['success'] is True
    
    # Check if cookie is set
    cookie = client.get_cookie('access_token_cookie')
    assert cookie is not None
    # assert cookie.secure == False # In testing (not prod) might be false depending on config

    # 3. Check Auth (should be authorized now)
    response = client.get('/api/check-auth')
    assert response.status_code == 200
    assert response.json['authenticated'] is True

    # 4. Logout
    response = client.post('/api/logout')
    assert response.status_code == 200
    
    # Check Auth again (should be unauthorized)
    response = client.get('/api/check-auth')
    assert response.status_code == 401

def test_login_invalid_password(client, app):
    """Test login with wrong password"""
    
    # Seed Admin
    password = "correctpassword"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with app.app_context():
        admin = AdminInfo(password_hash=hashed)
        db.session.add(admin)
        db.session.commit()

    # Attempt login
    response = client.post('/api/login', json={'password': "wrongpassword"})
    assert response.status_code == 401
