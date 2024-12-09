from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# This define the WastePickup model
class WastePickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    waste_type = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pickup_day = db.Column(db.String(100), nullable=False)
    pickup_time = db.Column(db.String(100), nullable=False)

