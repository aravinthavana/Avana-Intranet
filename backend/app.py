import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '../frontend/dist')

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/')
CORS(app)  # Enable CORS for development

# Helper to read/write JSON
def read_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def write_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# API Endpoints

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    # Simple hardcoded password for now (Production note: use env vars or hash)
    if data.get('password') == 'admin123':
        return jsonify({'success': True, 'token': 'dummy-token'})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# --- Intercom ---
@app.route('/api/intercom', methods=['GET'])
def get_intercom():
    return jsonify(read_json('intercom.json'))

@app.route('/api/intercom', methods=['POST'])
def update_intercom():
    # Expects full list or single item? Let's assume full list replacement for simplicity in JSON for now,
    # or we can do append. Admin usually wants to edit.
    # For simplicity, let's accept the full list to overwrite.
    data = request.json
    write_json('intercom.json', data)
    return jsonify({'success': True})

# --- Announcements ---
@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    return jsonify(read_json('announcements.json'))

@app.route('/api/announcements', methods=['POST'])
def update_announcements():
    data = request.json
    write_json('announcements.json', data)
    return jsonify({'success': True})

# --- Events ---
@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(read_json('events.json'))

@app.route('/api/events', methods=['POST'])
def update_events():
    data = request.json
    write_json('events.json', data)
    return jsonify({'success': True})

# --- Bookings ---
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(read_json('bookings.json'))

@app.route('/api/bookings', methods=['POST'])
def update_bookings():
    data = request.json
    write_json('bookings.json', data)
    return jsonify({'success': True})

# --- Email Groups ---
@app.route('/api/email-groups', methods=['GET'])
def get_email_groups():
    return jsonify(read_json('email_groups.json'))

@app.route('/api/email-groups', methods=['POST'])
def update_email_groups():
    data = request.json
    write_json('email_groups.json', data)
    return jsonify({'success': True})


# Serve Frontend (Catch-all for SPA)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Return index.html for SPA routing
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return "Frontend not built yet. Run 'npm run build' in frontend folder.", 404

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible on network
    app.run(host='0.0.0.0', port=5000, debug=True)
