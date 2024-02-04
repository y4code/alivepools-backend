from flask import Flask, jsonify
import requests


app = Flask(__name__)

# @xuyao this should not be a api
@app.route("/send_email")
def send_simple_message():
    response = requests.post(
        "https://api.mailgun.net/v3/sandboxab84a42814d340b1929b218768aad10b.mailgun.org/messages",
        auth=("api", "295f28d50ca255514092639499d9a3e7-69a6bd85-62aa9be9"),  # Use your actual API key here, and make sure not to expose it publicly
        data={
            "from": "Excited User <mailgun@sandboxab84a42814d340b1929b218768aad10b.mailgun.org>",
            "to": ["yaoyishi@gmail.com"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!"
        })

    # Check if the request to Mailgun was successful
    if response.status_code == 200:
        return "Email sent successfully!"
    else:
        # Returning a simple error message and status code if the request failed
        return jsonify({"error": "Failed to send email", "details": response.text}), 500

def send_custom_message():
    recipient = request.args.get('recipient')
    subject = request.args.get('subject')
    message = request.args.get('message')

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