from flask import Flask, request, jsonify, Blueprint
import requests

# Create a blueprint
bp = Blueprint('domain', __name__)

@bp.route("/domain", methods=["GET"])
def check_by_domain():
    website = request.args.get("website")
    try:
        response = requests.get("http://" + website)
        # If the GET request is successful, the website is available
        if response.status_code == 200:
            return jsonify({"message": "Website is available"}), 200
        else:
            # If the server returns a status code other than 200, it's considered unavailable for this purpose
            return jsonify({"message": "Website not found"}), 404
    except requests.exceptions.RequestException:
        # If the GET request fails (e.g., due to a network problem or invalid URL), the website is considered not found
        return jsonify({"message": "Website not found"}), 404