import bcrypt
import os

# Generate hash for admin123
password = b'admin123'
hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

# Create .env content
env_content = f"""# Flask Configuration
FLASK_SECRET_KEY=dev-secret-key-change-in-production-12345
FLASK_ENV=development
FLASK_DEBUG=True

# JWT Configuration  
JWT_SECRET=dev-jwt-secret-change-in-production-67890
JWT_EXPIRATION_HOURS=24

# Admin Credentials
# Default password is: admin123
# Hash generated with bcrypt
ADMIN_PASSWORD_HASH={hashed}

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://localhost:5000

# Data Directory
DATA_DIR=./data

# Backup Settings
BACKUP_ENABLED=True
BACKUP_RETENTION_DAYS=30
"""

# Write to .env file
with open('.env', 'w') as f:
    f.write(env_content)

print(f"✓ Created .env file with password hash for 'admin123'")
print(f"✓ Hash: {hashed}")
