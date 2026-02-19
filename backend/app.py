import os
import secrets
from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import init_db

# Load environment variables
load_dotenv()

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '../frontend/dist')

# Initialize Limiter
limiter = Limiter(
    key_func=get_remote_address,
    # Increased limits for intranet usage
    default_limits=["2000 per day", "500 per hour"],
    storage_uri="memory://"
)

def create_app():
    app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/')
    
    # Security: Ensure strong secret key in production
    env_secret = os.getenv('FLASK_SECRET_KEY')
    if not env_secret:
        if os.getenv('FLASK_ENV') == 'production':
            # Strict enforcement in production
            raise ValueError("No FLASK_SECRET_KEY set for production environment")
        
        # Dev fallback
        app.logger.warning("Using insecure default SECRET_KEY. Set FLASK_SECRET_KEY in .env")
        app.config['SECRET_KEY'] = 'dev-secret-key'
    else:
        app.config['SECRET_KEY'] = env_secret

    # JWT Secret
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret:
        if os.getenv('FLASK_ENV') == 'production':
            raise ValueError("No JWT_SECRET_KEY set for production environment")
        app.config['JWT_SECRET_KEY'] = 'dev-jwt-fallback-key'
    else:
        app.config['JWT_SECRET_KEY'] = jwt_secret

    # Initialize Extensions
    init_db(app)
    limiter.init_app(app)

    # Configure CORS
    # In production, this should be set to the actual domain(s)
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5000').split(',')
    CORS(app, origins=cors_origins, supports_credentials=True)

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.intercom_routes import intercom_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(intercom_bp, url_prefix='/api')

    # Security Headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # CSP: Allow self, scripts/styles from self (and inline if needed for Vue/Vite dev, though purely static usually fine)
        # Adjust as needed later
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:;"
        
        # Strict-Transport-Security (HSTS) - Uncomment for HTTPS production
        # if os.getenv('FLASK_ENV') == 'production':
        #     response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({'error': f'Rate limit exceeded: {e.description}'}), 429

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f'Unhandled exception: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

    # Frontend Serving
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            if os.path.exists(os.path.join(app.static_folder, 'index.html')):
                return send_from_directory(app.static_folder, 'index.html')
            else:
                return jsonify({'error': 'Frontend not built'}), 404

    return app, limiter

if __name__ == '__main__':
    app, _ = create_app()
    
    # Ensure data directory exists (for SQLite file)
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
