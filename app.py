from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from sms_service import SMS

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waste_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create the database and tables
with app.app_context():
    db.create_all()

# Initialize Africa's Talking with environment variables
username = os.getenv('AFRICASTALKING_USERNAME', 'USERNAME_HERE')
api_key = os.getenv('AFRICASTALKING_API_KEY', 'API_KEY_HERE')

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

    if text == '':
        response = "CON Welcome to Pick Waste Solutions:\n"
        response += "1) Residential Waste Collection\n"
        response += "2) Commercial Waste Collection\n"
        response += "3) Construction and Demolition Waste\n"
        response += "4) Hazardous Waste Disposal\n"
        session['step'] = 1
    elif session['step'] == 1:
        options = {
            '1': 'Residential Waste Collection',
            '2': 'Commercial Waste Collection',
            '3': 'Construction and Demolition Waste',
            '4': 'Hazardous Waste Disposal'
        }

        if latest_input in options:
            session['waste_service'] = options[latest_input]
            current_pickup.waste_type = session['waste_service']  # This line save the service type here when a user enter data
            db.session.commit()
            response = f"CON {session['waste_service']} selected.\n"
            response += "Choose Waste Type:\n"
            response += "1) Solid Waste\n"
            response += "2) Liquid Waste\n"
            session['step'] = 2
        else:
            response = "END Invalid option. Please try again."
            session['step'] = 0
            return response
    elif session['step'] == 2:
        waste_types = {
            '1': 'Solid Waste',
            '2': 'Liquid Waste'
        }

        if latest_input in waste_types:
            session['waste_type'] = waste_types[latest_input]
            current_pickup.waste_type = session['waste_type']
            db.session.commit()
            response = "CON Enter Address to Pick the Waste:\n"
            session['step'] = 3
        else:
            response = "CON Invalid option. Please select the waste type:\n"
            response += "1) Solid Waste\n"
            response += "2) Liquid Waste\n"
    elif session['step'] == 3:
        session['address'] = text.lstrip('1234567890* ')
        current_pickup.address = session['address']
        db.session.commit()
        response = "CON Select Pickup Day:\n"
        response += "1) Monday\n"
        response += "2) Tuesday\n"
        response += "3) Wednesday\n"
        response += "4) Thursday\n"
        response += "5) Friday\n"
        response += "6) Sunday\n"
        session['step'] = 4
    elif session['step'] == 4:
        days = {
            '1': 'Monday',
            '2': 'Tuesday',
            '3': 'Wednesday',
            '4': 'Thursday',
            '5': 'Friday',
            '6': 'Sunday'
        }

        if latest_input in days:
            session['pickup_day'] = days[latest_input]
            current_pickup.pickup_day = session['pickup_day']
            db.session.commit()
            response = f"CON Pickup day set: {session['pickup_day']}\n"
            response += "Select Pickup Time:\n"
            response += "1) 8:00 AM - 10:00 AM\n"
            response += "2) 10:00 AM - 12:00 PM\n"
            response += "3) 12:00 PM - 2:00 PM\n"
            response += "4) 2:00 PM - 4:00 PM\n"
            response += "5) 4:00 PM - 6:00 PM\n"
            session['step'] = 5
        else:
            response = "CON Invalid option. Please select a pickup day:\n"
            response += "1) Monday\n"
            response += "2) Tuesday\n"
            response += "3) Wednesday\n"
            response += "4) Thursday\n"
            response += "5) Friday\n"
            response += "6) Sunday\n"
    elif session['step'] == 5:
        times = {
            '1': '8:00 AM - 10:00 AM',
            '2': '10:00 AM - 12:00 PM',
            '3': '12:00 PM - 2:00 PM',
            '4': '2:00 PM - 4:00 PM',
            '5': '4:00 PM - 6:00 PM'
        }

        if latest_input in times:
            session['pickup_time'] = times[latest_input]
            current_pickup.pickup_time = session['pickup_time']
            db.session.commit()

            detailed_message = (
                f"Your waste pickup request was sent successfully.\n"
                f"Details are as follows:\n"
                f"{session['waste_service']}\n"
                f"Type of Waste: {session['waste_type']}\n"
                f"Your Address: {session['address']}\n"
                f"Pickup day: {session['pickup_day']}\n"
                f"Pickup time: {session['pickup_time']}\n"
                f"Thank you for using our services! Customer Care: +256787927092, +211925413115\n"
                f"Pick Waste Solutions. Empowering Communities for a Cleaner Tomorrow"
            )

            # Send SMS to the dynamic phone number
            sms_service.send(detailed_message, [phone_number])

            response = "END Your Waste Pickup request has been submitted. Thank you for using our services!"
            user_sessions.pop(session_id, None)
        else:
            response = "CON Invalid option. Please select a pickup time:\n"
            response += "1) 8:00 AM - 10:00 AM\n"
            response += "2) 10:00 AM - 12:00 PM\n"
            response += "3) 12:00 PM - 2:00 PM\n"
            response += "4) 2:00 PM - 4:00 PM\n"
            response += "5) 4:00 PM - 6:00 PM\n"
    else:
        response = "END Invalid input. Please try again."

    return response

@app.route("/view_data", methods=['GET'])
def view_data():
    pickups = WastePickup.query.all()
    results = [
        {
            "phone_number": pickup.phone_number,
            "waste_type": pickup.waste_type,
            "address": pickup.address,
            "pickup_day": pickup.pickup_day,
            "pickup_time": pickup.pickup_time
        } for pickup in pickups]

    return jsonify({"pickups": results}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
