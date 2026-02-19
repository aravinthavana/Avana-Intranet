"""
Marshmallow schemas for input validation
"""
from marshmallow import Schema, fields, validate, ValidationError, EXCLUDE

class IntercomPersonSchema(Schema):
    """Schema for intercom directory person validation"""
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    designation = fields.Str(load_default="", validate=validate.Length(max=100))
    extension = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    floor = fields.Str(required=True, validate=validate.OneOf([
        'Ground Floor', '1st Floor', '2nd Floor', '3rd Floor', 'Other'
    ]))

class LoginSchema(Schema):
    """Schema for login validation"""
    password = fields.Str(required=True, validate=validate.Length(min=1, max=100))

class ChangePasswordSchema(Schema):
    """Schema for changing password"""
    old_password = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    new_password = fields.Str(required=True, validate=validate.Length(min=6, max=100))

def validate_request(schema_class):
    """Decorator to validate request data against a schema"""
    def decorator(f):
        from functools import wraps
        from flask import request, jsonify
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_class()
            try:
                # Validate request JSON
                validated_data = schema.load(request.json)
                # Add validated data to request context
                request.validated_data = validated_data
            except ValidationError as err:
                return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
            except Exception as e:
                return jsonify({'error': 'Invalid request data'}), 400
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
