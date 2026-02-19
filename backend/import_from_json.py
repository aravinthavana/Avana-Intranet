import json
import os
from app import create_app
from database import db, Intercom

def import_json_data():
    app, _ = create_app()
    with app.app_context():
        # Clear existing data (optional, but good for clean state)
        db.session.query(Intercom).delete()
        db.session.commit()
        print("Cleared existing data.")

        json_path = os.path.join(os.path.dirname(__file__), 'data', 'intercom.json')
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} not found.")
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        print(f"Found {len(data)} records to import.")

        people = []
        for item in data:
            # We can choose to preserve ID or let DB auto-increment.
            # Preserving ID is risky if they aren't unique or valid integers.
            # Map 'department' from JSON to 'designation' in DB
            person = Intercom(
                name=item.get('name'),
                designation=item.get('department'), 
                extension=str(item.get('extension')), # Ensure string
                floor=item.get('floor')
            )
            people.append(person)
        
        db.session.add_all(people)
        db.session.commit()
        print(f"✅ Successfully imported {len(people)} records from intercom.json!")

if __name__ == "__main__":
    import_json_data()
