from flask import Blueprint, request, jsonify, current_app
from database import db, Intercom
from schemas import IntercomPersonSchema
from auth import require_auth

intercom_bp = Blueprint('intercom', __name__)

@intercom_bp.route('/intercom', methods=['GET'])
def get_intercom():
    """Get intercom directory"""
    try:
        records = db.session.execute(db.select(Intercom).order_by(Intercom.name)).scalars().all()
        return jsonify({
            'data': [item.to_dict() for item in records],
            'count': len(records)
        })
    except Exception as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500

@intercom_bp.route('/intercom', methods=['POST'])
@require_auth
def add_person():
    """Add a new person to directory"""
    try:
        schema = IntercomPersonSchema()
        data = schema.load(request.json)
        
        person = Intercom(
            name=data.get('name'),
            designation=data.get('designation'),
            extension=data.get('extension'),
            floor=data.get('floor')
        )
        db.session.add(person)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Person added', 'data': person.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add error: {e}")
        return jsonify({'error': 'Failed to add person', 'details': str(e)}), 500

@intercom_bp.route('/intercom/<int:id>', methods=['PUT'])
@require_auth
def update_person(id):
    """Update an existing person"""
    try:
        person = db.session.get(Intercom, id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404

        schema = IntercomPersonSchema()
        data = schema.load(request.json)
        
        person.name = data.get('name')
        person.designation = data.get('designation')
        person.extension = data.get('extension')
        person.floor = data.get('floor')
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Person updated'})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update error: {e}")
        return jsonify({'error': 'Failed to update person', 'details': str(e)}), 500

@intercom_bp.route('/intercom/<int:id>', methods=['DELETE'])
@require_auth
def delete_person(id):
    """Delete a person from directory"""
    try:
        person = db.session.get(Intercom, id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404
            
        db.session.delete(person)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Person deleted'})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete error: {e}")
        return jsonify({'error': 'Failed to delete person', 'details': str(e)}), 500
