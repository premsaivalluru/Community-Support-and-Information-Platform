from twilio.rest import Client
import os
from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException

load_dotenv()

verify_sid = os.getenv("TWILIO_VERIFY_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
sender = os.getenv("TWILIO_PHONE_NUMBER")

def send_otp(phone):
    try:            
        client = Client(account_sid, auth_token)
        verification = client.verify.v2.services(verify_sid).verifications.create(
            to = phone,
            channel="sms"
        )
        return {"success": True, "message": "OTP sent successfully", 'status': verification.status}
    except TwilioRestException as e:
        print(f"Twilio Error: {e.msg}")
        return {"success": False, "message": f"{e.msg}", 'status': 500}

def verify_otp(phone,otp):
    try:
        client = Client(account_sid, auth_token)
        verification = client.verify.v2.services(verify_sid).verification_checks.create(
            to = phone,
            code= otp
        )
        if verification.status == "approved":
            return {"success": True, "message": "Phone Number Verified!"} 
    except TwilioRestException as e:
        return {"success": False, "message": "Wrong OTP Enetered!!", 'status':400}

def send_message(phone, message_post):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_post,
            from_ = sender,
            to=phone
        )
        return {"success": True, "message" : "Message sent successfully!", "sid": message.sid}
    except TwilioRestException as e:
        return {"success" : False, "message" : f"{e.msg}"}