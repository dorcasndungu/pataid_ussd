import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request
import africastalking
import os

app = Flask(__name__)

# Initialize Firebase app with credentials
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ussd-79318-default-rtdb.firebaseio.com/'
})

username = "dorcaslovelacegirl"
api_key = "b0af8e9fa3ed67824380c6c2ab5c0139bece3e7e496f1bbe00366d340ffdfe21"
africastalking.initialize(username, api_key)
sms = africastalking.SMS
# Define the reference to the Firebase Realtime Database
ref = db.reference()

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)
    session_data = {}
    # ussd logic
    # main menu
    if text == '':
        response = "CON Welcome to Pata ID! \n Please choose a service \n"
        response += "1. Report Lost ID \n"
        response += "2. Report Found ID"

    # Handling the menu options
    elif text.startswith('1'):
    # If option 1 is selected, prompt the user to enter their ID number
        response = "CON Please enter your ID number:"
    # Save the current step in the session data
        session_data['step'] = 'enter_id_number'
    elif session_data.get('step') == 'enter_id_number':
    # If the user is in the process of entering their ID number
    # Extract the ID number from the user's input
        id_number = text
    # Prompt the user to enter the name as on the ID
        response = "CON Please enter the name as on the ID:"
    # Save the ID number in the session data
        session_data['id_number'] = id_number
    # Update the session step
        session_data['step'] = 'enter_name'
    elif session_data.get('step') == 'enter_name':
    # If the user is in the process of entering their name
    # Extract the name input from the user's input
        name = text
    # Process the ID number and name here
    # You can save them to a database or perform any necessary operations
    # Access the ID number from session data
        id_number = session_data.get('id_number')
         # Save data to Firebase under "lost_id" node
        ref.child('lost_id').push({
            'id_number': session_data['id_number'],
            'name': name
        })
    # Clear session data
        session_data.clear()
        response = "END Report submitted successfully. We will notify you when it is found. Thank you!"

    elif text.startswith('2'):
    # If option 2 is selected, prompt the user to enter the ID number found
        response = "CON Please enter the ID number found:"
    # Save the current step in the session data
        session_data['step'] = 'enter_id_number_found'
    elif session_data.get('step') == 'enter_id_number_found':# If the user is in the process of reporting a found ID
    # Extract the ID number found from the user's input
        id_number_found = text
    # Prompt the user to enter the name as on the ID
        response = "CON Please enter the name as on the ID:"
    # Save the ID number found in the session data
        session_data['id_number_found'] = id_number_found
    # Update the session step
        session_data['step'] = 'enter_name_found'
    elif session_data.get('step') == 'enter_name_found':
    # If the user is in the process of reporting a found ID
    # Extract the name input from the user's input
        name_found = text
    # Prompt the user to enter the location found
        response = "CON Please enter the location found:"
    # Save the name as on the ID in the session data
        session_data['name_found'] = name_found
    # Update the session step
        session_data['step'] = 'enter_location_found'
    elif session_data.get('step') == 'enter_location_found':
    # If the user is in the process of reporting a found ID
    # Extract the location found input from the user's input
        location_found = text
    # Save data to Firebase under "found_id" node
        ref.child('found_id').push({
            'id_number_found': session_data['id_number_found'],
            'name_found': session_data['name_found'],
            'location_found': location_found
        })
    # Clear session data
        session_data.clear()
        response = "END Report submitted successfully. Thank you!"

    else:
        response = "END Invalid input. Try again."

    # Store session data in Firebase
    ref.child('session_data').child(session_id).set(session_data)

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 3000)