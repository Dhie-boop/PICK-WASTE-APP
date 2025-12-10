# Pick Waste Solutions
Pick Waste Solutions is a mobile and USSD-based application built with Flask and powered by SQLAlchemy for database management. It leverages USSD technology integrated with the Africa's Talking API to provide a seamless, text-based interface for waste collection services.


## Getting Started with Pick Waste Solutions
Before you begin, you'll need the following tools installed on your system:

* Python 3.10+
* Git
* Virtual Environment Tools (e.g., venv)
* PostgreSQL or SQLite
* An Africa's Talking API Account

## Installation and Setup
1. **Clone the Repository**

   ```bash
   git clone [https://github.com/username/PICK-WASTE-APP]
   cd PICK-WASTE-APP
2. **Set Up a Virtual Environment**
* python -m venv venv
* source venv/bin/activate  ``` On Windows: venv\Scripts\activate ```

3. **Install Dependencies**
```pip install -r requirements.txt ```

4. **Set Up Environment Variables**
   Create a file named ```.env``` in the project's root directory and add the following lines, replacing the placeholders with your actual credentials:
   
   ```app.py
      FLASK_APP=app.py
      FLASK_ENV=development
      AFRICASTALKING_USERNAME=your_africas_talking_username
      AFRICASTALKING_API_KEY=your_africas_talking_api_key
      DATABASE_URL=sqlite:///db.sqlite3  # Update for PostgreSQL
      SECRET_KEY=your_secret_key
      DEBUG=True
      USSD_CODE SHARED SERVICE CODE ``` 
5. **Database Migration**
     Initialize the database using SQLAlchemy:
     ```termainal
        flask db
        flask db migrate -m "Initial migration"
        flask db upgrade

6. **Run the Application**
     ```terminal
        flask run
        The application will be accessible at http://127.0.0.1:5000.


## Simulating the USSD on Localhost
To test the USSD app locally, use Ngrok to expose your Flask server:

1. **Install Ngrok:**
   ``` bash
       brew instal ngrok # On Mac
       choco install ngrok  # On Windows
2. **Start Ngrok on the Flask port:**
   ``` bash
       ngrok http 5000
3. **Copy the Ngrok URL (e.g., https://abc123.ngrok.io) and set it in your Africa's Talking callback settings for your USSD app.**

## How the USSD Works

1. **User Interaction:**
   * The user dials the USSD code (e.g., *123#) on their mobile phone.
   * Menu options appear for scheduling pickups, payments, or checking service status.
2. **Request Handling:**
   * Africa's Talking forwards user inputs to the Flask app via callbacks.
   * Flask processes the request, interacts with the database using SQLAlchemy, and returns a response to the user.
3. **Database Usage:**
   * QLAlchemy handles waste collection records, user data, and payment tracking.



## Next Steps
1. **Integrate with Mobile Money:**
   * Add payment processing through Africa's Talking mobile money APIs.

**With Pick Waste Solutions, communities can benefit from an affordable, accessible, and efficient waste management system. 🌱*
