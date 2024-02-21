# 域名的可用性检查

from flask import Flask, request, jsonify, Blueprint
import requests

# Create a blueprint
bp = Blueprint("domain_api", __name__)


@bp.route("/domain", methods=["POST"])
def check_by_domain():
    website = request.json.get("website")
    try:
        for _ in range(5):
            response = requests.get("http://" + website)
            # If the GET request is successful, the website is available
            if response.status_code == 200:
                return jsonify({"message": "Website is available"}), 200
        # If all requests fail, the website is considered not available
        return jsonify({"message": "Website is not available"}), 200
    except requests.exceptions.RequestException:
        # If the GET request fails (e.g., due to a network problem or invalid URL), the website is considered not found
        return jsonify({"message": "Website not found"}), 200