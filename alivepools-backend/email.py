# 邮件的模版和发送

from flask import Flask, jsonify, Blueprint, request
import requests

# Create a blueprint object
bp = Blueprint('email', __name__)

# Define another route within the blueprint
def send_custom_email(recipient, subject, message):
    print(f"Sending email to {recipient} with subject {subject} and message {message}")
    response = requests.post(
        "https://api.mailgun.net/v3/sandboxab84a42814d340b1929b218768aad10b.mailgun.org/messages",
        auth=("api", "295f28d50ca255514092639499d9a3e7-69a6bd85-62aa9be9"),
        data={
            "from": "Excited User <mailgun@sandboxab84a42814d340b1929b218768aad10b.mailgun.org>",
            "to": [recipient],
            "subject": subject,
            "text": message
        })

    if response.status_code == 200:
        return "Email sent successfully!"
    else:
        return jsonify({"error": "Failed to send email", "details": response.text}), 500