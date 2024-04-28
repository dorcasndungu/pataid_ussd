import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request
import africastalking


app = Flask(__name__)  # Corrected the variable name

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
        # Retrieve session data from Firebase Realtime Database
    session_data = ref.child(session_id).get() or {}
    # ussd logic
    # main menu
    if text == '':
        response = "CON Welcome to Pata ID! \n Please choose a service \n"
        response += "1. Report Lost ID \n"
        response += "2. Report Found ID"

    # Handling the menu options
    elif text == '1':
        response = "CON Please enter your ID number:"
        session_data['step'] = 'enter_id_number'

    elif session_data.get('step') == 'enter_id_number':
        session_data['id_number'] = text
        response = "CON Please enter the name as on the ID:"
        session_data['step'] = 'enter_name'

    elif session_data.get('step') == 'enter_name':
        session_data['name'] = text
        ref.child(session_id).update(session_data)  # Update session data in Firebase
        ref.child('lost_id').push(session_data)  # Save data to Firebase under "lost_id" node
        response = "END Report submitted successfully. We will notify you when it is found. Thank you!"

    elif text == '2':
        response = "CON Please enter the ID number found:"
        session_data['step'] = 'enter_id_number_found'

    elif session_data.get('step') == 'enter_id_number_found':
        session_data['id_number_found'] = text
        response = "CON Please enter the name as on the ID:"
        session_data['step'] = 'enter_name_found'

    elif session_data.get('step') == 'enter_name_found':
        session_data['name_found'] = text
        response = "CON Please enter the location found:"
        session_data['step'] = 'enter_location_found'

    elif session_data.get('step') == 'enter_location_found':
        session_data['location_found'] = text
        ref.child(session_id).update(session_data)  # Update session data in Firebase
        ref.child('found_id').push(session_data)  # Save data to Firebase under "found_id" node
        response = "END Report submitted successfully. Thank you!"


    else:
        response = "END Invalid input. Try again."

    return response

if __name__ == "__main__":  # Corrected the variable name
    app.run(host="0.0.0.0", port= 3000)
