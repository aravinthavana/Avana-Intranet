"""
Authentication utilities for Office Intranet
Handles JWT token generation, validation, and password hashing
"""
import os
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
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

def generate_token(user_id) -> str:
    """Generate a JWT token"""
    expiration = datetime.now(timezone.utc) + timedelta(
        hours=float(os.getenv('JWT_EXPIRATION_HOURS', 24))
    )
    
    payload = {
        'sub': user_id,
        'exp': expiration,
        'iat': datetime.now(timezone.utc)
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
        token = None
        
        # 1. Check Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        # 2. Check Cookie (if no header)
        if not token:
            token = request.cookies.get('access_token_cookie')

        if not token:
            return jsonify({'error': 'No authorization token provided'}), 401
        
        try:
            payload = decode_token(token)
            
            # Add user info to request context
            request.user = payload
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
