from app import create_app
from database import db, AdminInfo
from auth import hash_password

new_password = "ITAdmin@Avana"

app, _ = create_app()

with app.app_context():
    admin = db.session.execute(db.select(AdminInfo)).scalar_one_or_none()
    
    if admin:
        admin.password_hash = hash_password(new_password)
        db.session.commit()
        print("Successfully updated existing admin password to ITAdmin@Avana")
    else:
        # Create it if it doesn't exist
        new_admin = AdminInfo(password_hash=hash_password(new_password))
        db.session.add(new_admin)
        db.session.commit()
        print("Created new admin account with password ITAdmin@Avana")
