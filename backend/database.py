from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text
import os

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Intercom(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    designation: Mapped[str] = mapped_column(String(100), nullable=True)
    extension: Mapped[str] = mapped_column(String(20), nullable=False)
    floor: Mapped[str] = mapped_column(String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation,
            'extension': self.extension,
            'floor': self.floor
        }

class AdminInfo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

def init_db(app):
    # Configure SQLite database
    # Use instance path if available, otherwise relative to this file
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'office_intranet.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
