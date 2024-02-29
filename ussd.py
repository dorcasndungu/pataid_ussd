# import firebase_admin
# from firebase_admin import credentials, db
# cred = credentials.Certificate("C:\Users\pc\OneDrive\Desktop\Pata_id\credentials.json")
# firebase_admin.initialize_app(cred, {'databaseURL': 'https://pataid-default-rtdb.firebaseio.com'})
from flask import Flask, request
import africastalking
import os

app = Flask(_name_)  # Corrected the variable name

username = "sandbox"
api_key = ""
africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)

    # ussd logic
    # main menu
    if text == '':
        response = "CON Welcome to Pata_ID! What do you want? \n"
        response += "1. Report Lost ID \n"
        response += "2. Report Found ID"

    # Handling the menu options
    elif text == '1':
        response = "CON Please enter your ID number\n"

    elif text == '1*':
        response = "CON Please enter the name as on the ID\n"

    elif text == '1**':
        response = "END Report submitted successfully. We will notify you when it is found. Thank you!"

    elif text == '2':
        response = "CON Please enter the ID number found\n"

    elif text == '2*':
        response = "CON Please enter the name as on the ID\n"

    elif text == '2**':
        response = "CON Please enter the location found\n"

    elif text == '2***':
        response = "END Report submitted successfully. Thank you!"

    else:
        response = "END Invalid input. Try again."

    return response

if _name_ == "main":  # Corrected the variable name
    app.run(host="0.0.0.0", port= 3000)
