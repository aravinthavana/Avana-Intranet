"""
Marshmallow schemas for input validation
"""
from marshmallow import Schema, fields, validate, ValidationError

class AnnouncementSchema(Schema):
    """Schema for announcement validation"""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
    date = fields.Date(required=True)
    important = fields.Bool(missing=False)

class IntercomPersonSchema(Schema):
    """Schema for intercom directory person validation"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    department = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    extension = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    floor = fields.Str(required=True, validate=validate.OneOf([
        'Ground Floor', '1st Floor', '2nd Floor', '3rd Floor', 'Other'
    ]))

class EventSchema(Schema):
    """Schema for event validation"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    date = fields.Date(required=True)
    time = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    location = fields.Str(required=True, validate=validate.Length(min=1, max=200))

class BookingSchema(Schema):
    """Schema for hall booking validation"""
    id = fields.Int(dump_only=True)
    hall = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    booked_by = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    date = fields.Date(required=True)
    start_time = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    end_time = fields.Str(required=True, validate=validate.Length(min=1, max=10))

class EmailGroupSchema(Schema):
    """Schema for email group validation"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)

class LoginSchema(Schema):
    """Schema for login validation"""
    password = fields.Str(required=True, validate=validate.Length(min=1, max=100))

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
