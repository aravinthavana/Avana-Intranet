import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Import our modules
from auth import require_auth, verify_password, generate_token
from utils import read_json_safe, write_json_safe
from schemas import (
    LoginSchema, AnnouncementSchema, IntercomPersonSchema,
    EventSchema, BookingSchema, EmailGroupSchema, validate_request
)

# Configuration
DATA_DIR = os.getenv('DATA_DIR', './data')
if not os.path.isabs(DATA_DIR):
    DATA_DIR = os.path.join(os.path.dirname(__file__), DATA_DIR)

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '../frontend/dist')

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5000').split(',')
CORS(app, origins=cors_origins)

# Helper functions
def get_data_path(filename):
    """Get full path for data file"""
    return os.path.join(DATA_DIR, filename)

# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.route('/api/login', methods=['POST'])
@validate_request(LoginSchema)
def login():
    """
    Authenticate admin user and return JWT token
    """
    password = request.validated_data.get('password')
    admin_hash = os.getenv('ADMIN_PASSWORD_HASH')
    
    if not admin_hash:
        return jsonify({'error': 'Server configuration error'}), 500
    
    if verify_password(password, admin_hash):
        token = generate_token('admin')
        return jsonify({
            'success': True,
            'token': token,
            'message': 'Login successful'
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

# ============================================================================
# Public Endpoints (Read-only, no authentication required)
# ============================================================================

@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    """Get all announcements"""
    data = read_json_safe(get_data_path('announcements.json'))
    return jsonify(data)

@app.route('/api/intercom', methods=['GET'])
def get_intercom():
    """Get intercom directory"""
    data = read_json_safe(get_data_path('intercom.json'))
    return jsonify(data)

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    data = read_json_safe(get_data_path('events.json'))
    return jsonify(data)

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Get all bookings"""
    data = read_json_safe(get_data_path('bookings.json'))
    return jsonify(data)

@app.route('/api/email-groups', methods=['GET'])
def get_email_groups():
    """Get email groups"""
    data = read_json_safe(get_data_path('email_groups.json'))
    return jsonify(data)

# ============================================================================
# Protected Endpoints (Require authentication)
# ============================================================================

@app.route('/api/announcements', methods=['POST'])
@require_auth
def update_announcements():
    """Update announcements (admin only)"""
    data = request.json
    
    # Validate each announcement
    schema = AnnouncementSchema(many=True)
    try:
        validated = schema.load(data)
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'details': str(e)}), 400
    
    success = write_json_safe(get_data_path('announcements.json'), validated)
    
    if success:
        return jsonify({'success': True, 'message': 'Announcements updated'})
    return jsonify({'error': 'Failed to save data'}), 500

@app.route('/api/intercom', methods=['POST'])
@require_auth
def update_intercom():
    """Update intercom directory (admin only)"""
    data = request.json
    
    # Validate each person
    schema = IntercomPersonSchema(many=True)
    try:
        validated = schema.load(data)
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'details': str(e)}), 400
    
    success = write_json_safe(get_data_path('intercom.json'), validated)
    
    if success:
        return jsonify({'success': True, 'message': 'Intercom directory updated'})
    return jsonify({'error': 'Failed to save data'}), 500

@app.route('/api/events', methods=['POST'])
@require_auth
def update_events():
    """Update events (admin only)"""
    data = request.json
    
    # Validate each event
    schema = EventSchema(many=True)
    try:
        validated = schema.load(data)
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'details': str(e)}), 400
    
    success = write_json_safe(get_data_path('events.json'), validated)
    
    if success:
        return jsonify({'success': True, 'message': 'Events updated'})
    return jsonify({'error': 'Failed to save data'}), 500

@app.route('/api/bookings', methods=['POST'])
@require_auth
def update_bookings():
    """Update bookings (admin only)"""
    data = request.json
    
    # Validate each booking
    schema = BookingSchema(many=True)
    try:
        validated = schema.load(data)
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'details': str(e)}), 400
    
    success = write_json_safe(get_data_path('bookings.json'), validated)
    
    if success:
        return jsonify({'success': True, 'message': 'Bookings updated'})
    return jsonify({'error': 'Failed to save data'}), 500

@app.route('/api/email-groups', methods=['POST'])
@require_auth
def update_email_groups():
    """Update email groups (admin only)"""
    data = request.json
    
    # Validate each email group
    schema = EmailGroupSchema(many=True)
    try:
        validated = schema.load(data)
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'details': str(e)}), 400
    
    success = write_json_safe(get_data_path('email_groups.json'), validated)
    
    if success:
        return jsonify({'success': True, 'message': 'Email groups updated'})
    return jsonify({'error': 'Failed to save data'}), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected errors"""
    app.logger.error(f'Unhandled exception: {str(e)}')
    return jsonify({'error': 'An unexpected error occurred'}), 500

# ============================================================================
# Frontend Serving (Catch-all for SPA)
# ============================================================================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve frontend static files"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Return index.html for SPA routing
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({
                'error': 'Frontend not built',
                'message': "Run 'npm run build' in frontend folder"
            }), 404

# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Run server
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
