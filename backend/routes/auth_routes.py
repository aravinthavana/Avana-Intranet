from flask import Blueprint, request, jsonify
from auth import verify_password, generate_token, hash_password, require_auth
from schemas import LoginSchema, ChangePasswordSchema, validate_request
from database import db, AdminInfo
from app import limiter
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute") # Strict limit for login attempts
@validate_request(LoginSchema)
def login():
    """Authenticate admin user and return JWT token"""
    password = request.validated_data.get('password')
    
    # Check DB for admin info
    admin = db.session.execute(db.select(AdminInfo)).scalar_one_or_none()
    
    # Initialization: If no admin in DB, seed from env
    if not admin:
        env_password = os.getenv('ADMIN_PASSWORD')
        env_hash = os.getenv('ADMIN_PASSWORD_HASH')
        
        if env_password:
             # Seed with plain text password (hashed on the fly)
             new_admin = AdminInfo(password_hash=hash_password(env_password))
        elif env_hash:
             # Seed with pre-hashed password
             new_admin = AdminInfo(password_hash=env_hash)
        else:
             return jsonify({'error': 'Server configuration error: No admin password configured'}), 500
        
        db.session.add(new_admin)
        db.session.commit()
        admin = new_admin

    if verify_password(password, admin.password_hash):
        token = generate_token('admin')
        
        response = jsonify({
            'success': True, 
            'message': 'Login successful',
            'token': token  # Return token in body for Bearer auth
        })
        
        # Also set cookie as fallback (not relied upon for UI state)
        response.set_cookie(
            'access_token_cookie',
            token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        return response
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout admin by clearing cookie"""
    response = jsonify({'success': True, 'message': 'Logged out successfully'})
    response.set_cookie('access_token_cookie', '', expires=0, httponly=True, path='/')
    return response

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """
    Verify if the user is authenticated via cookie.
    Returns 200 OK with {'authenticated': False} if not logged in,
    to avoid browser console 401 errors.
    """
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
        return jsonify({'authenticated': False})
    
    try:
        # We need to import decode_token inside to avoid circular imports 
        # or just import it at top provided auth.py is clean.
        from auth import decode_token
        payload = decode_token(token)
        return jsonify({'authenticated': True, 'user': payload})
    except Exception:
        return jsonify({'authenticated': False})

@auth_bp.route('/change-password', methods=['PUT'])
@require_auth
@limiter.limit("5 per minute")
@validate_request(ChangePasswordSchema)
def change_password():
    """Change admin password"""
    data = request.validated_data
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    admin = db.session.execute(db.select(AdminInfo)).scalar_one_or_none()
    
    if not admin:
        return jsonify({'error': 'Admin account not found'}), 404
        
    if not verify_password(old_password, admin.password_hash):
        return jsonify({'error': 'Incorrect old password'}), 400
        
    # Update password
    admin.password_hash = hash_password(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password updated successfully'})
