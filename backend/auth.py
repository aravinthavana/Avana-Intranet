"""
Authentication utilities for Office Intranet
Handles JWT token generation, validation, and password hashing
"""
import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def generate_token(user_id: str = 'admin') -> str:
    """Generate a JWT token"""
    expiration = datetime.utcnow() + timedelta(
        hours=int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    )
    
    payload = {
        'user_id': user_id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    
    secret = os.getenv('JWT_SECRET', 'fallback-secret-key')
    return jwt.encode(payload, secret, algorithm='HS256')

def decode_token(token: str) -> dict:
    """Decode and validate a JWT token"""
    try:
        secret = os.getenv('JWT_SECRET', 'fallback-secret-key')
        return jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization token provided'}), 401
        
        try:
            # Expected format: "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({'error': 'Invalid authorization header format'}), 401
            
            token = parts[1]
            payload = decode_token(token)
            
            # Add user info to request context
            request.user = payload
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
