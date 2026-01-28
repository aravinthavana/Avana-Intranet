from app import app
from database import db, AdminInfo
from auth import hash_password
import sys

def reset_password(new_password="admin"):
    with app.app_context():
        admin = db.session.execute(db.select(AdminInfo)).scalar_one_or_none()
        
        hashed = hash_password(new_password)
        
        if admin:
            admin.password_hash = hashed
            print(f"✅ Existing admin password reset to: '{new_password}'")
        else:
            admin = AdminInfo(password_hash=hashed)
            db.session.add(admin)
            print(f"✅ Created new admin user with password: '{new_password}'")
            
        db.session.commit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        new_pass = sys.argv[1]
    else:
        new_pass = "admin123"
        
    print("⚠️  RESETTING ADMIN PASSWORD ⚠️")
    reset_password(new_pass)
