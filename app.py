from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from sms_service import SMS
from models import WastePickup

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waste_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create the database and tables
with app.app_context():
    db.create_all()

# Initialize Africa's Talking with environment variables
username = os.getenv('AFRICASTALKING_USERNAME', 'YOUR USER NAME HERE')
api_key = os.getenv('AFRICASTALKING_API_KEY', 'YOUR API KEY HERE')

sms_service = SMS(username, api_key)

# Store user sessions in a dictionary
user_sessions = {}

@app.route("/ussd", methods=['POST'])
def ussd():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "").strip()

    if session_id not in user_sessions:
        user_sessions[session_id] = {'step': 0, 'phone_number': phone_number}
        # Create a new WastePickup record with the phone number
        new_pickup = WastePickup(
            phone_number=phone_number,
            waste_type="",
            address="",
            pickup_day="",
            pickup_time=""
        )
        db.session.add(new_pickup)
        db.session.commit()

    session = user_sessions[session_id]

    # Retrieve the current pickup record for this session
    current_pickup = WastePickup.query.filter_by(phone_number=session['phone_number']).order_by(WastePickup.id.desc()).first()

    # Initialize response
    response = ""

    # Extract the latest input part for each step
    latest_input = text.split('*')[-1]
