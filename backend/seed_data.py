from app import create_app
from database import db, Intercom

def seed_intercom():
    app, _ = create_app()
    with app.app_context():
        # Check if empty
        if db.session.query(Intercom).count() > 0:
            print("Database already has data.")
            return

        print("Seeding data...")
        people = [
            Intercom(name="John Doe", department="IT", extension="101", floor="Ground Floor"),
            Intercom(name="Jane Smith", department="HR", extension="102", floor="1st Floor"),
            Intercom(name="Alice Johnson", department="Finance", extension="201", floor="2nd Floor"),
        ]
        
        db.session.add_all(people)
        db.session.commit()
        print("✅ Data seeded successfully!")

if __name__ == "__main__":
    seed_intercom()
