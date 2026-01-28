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
        env_hash = os.getenv('ADMIN_PASSWORD_HASH')
        if not env_hash:
             return jsonify({'error': 'Server configuration error'}), 500
        
        # Determine if env var is already a hash or plain text (simple check)
        # Assuming env var is HASHED as per previous conversation.
        # But if it's the first run and the user wants to "remove default", 
        # let's trust the env var is the initial seed hash.
        
        new_admin = AdminInfo(password_hash=env_hash)
        db.session.add(new_admin)
        db.session.commit()
        admin = new_admin

    if verify_password(password, admin.password_hash):
        token = generate_token('admin')
        return jsonify({
            'success': True, 
            'token': token,
            'message': 'Login successful'
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

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
