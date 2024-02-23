from flask import Flask, request, jsonify, Blueprint
import requests
from .response import (
    CODE_WEBSITE_NOT_AVAILABLE,
    CODE_WEBSITE_NOT_FOUND,
    response_ok,
    response_error,
)

bp = Blueprint("domain_api", __name__)


@bp.route("/domain", methods=["POST"])
def check_by_domain():
    website = request.json.get("website")
    try:
        for _ in range(5):
            response = requests.get("http://" + website)
            if response.status_code == 200:
                return response_ok(None)
        return response_error(None, CODE_WEBSITE_NOT_AVAILABLE, "Website not available")
    except requests.exceptions.RequestException:
        return response_error(None, CODE_WEBSITE_NOT_FOUND, "Website not found")
