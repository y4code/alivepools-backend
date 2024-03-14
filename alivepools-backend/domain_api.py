from flask import request, Blueprint
from .response import (
    CODE_WEBSITE_NOT_AVAILABLE,
    CODE_WEBSITE_NOT_FOUND,
    response_ok,
    response_error,
)
from .domain import check_website_availability

bp = Blueprint("domain_api", __name__)


@bp.route("/domain", methods=["POST"])
def check_by_domain():
    website = request.json.get("website")
    is_website_available = check_website_availability(website)
    if is_website_available:
        return response_ok(None)
    else:
        return response_error(None, CODE_WEBSITE_NOT_FOUND, "Website not found")
