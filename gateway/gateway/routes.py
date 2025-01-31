from flask import Blueprint, request, jsonify
import requests
from gateway.config import SERVICES
from gateway.logger import logger

bp = Blueprint('gateway', __name__)

@bp.route('/route/<service>', methods=['POST'])
def route_request(service):
    logger.info(f"🔍 Received request for {service}")
    logger.info(f"📥 Headers: {request.headers}")
    logger.info(f"📩 Data: {request.json}")

    if service not in SERVICES:
        logger.warning(f"❌ Service {service} not found")
        return jsonify({"error": "Service not found"}), 404

    data = request.json
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ModelHub-Client/1.0"
    }

    try:
        response = requests.post(SERVICES[service], json=data, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"🚨 Error calling {service}: {str(e)}")
        return jsonify({"error": "Service unavailable"}), 503

    logger.info(f"✅ Successfully routed request to {service}")
    return response.json(), response.status_code