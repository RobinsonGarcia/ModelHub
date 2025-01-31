from flask import Blueprint, request, jsonify
import requests
from gateway.config import SERVICES
from gateway.logger import logger

bp = Blueprint('gateway', __name__)

@bp.route('/route/<service>', methods=['POST'])
def route_request(service):
    if service not in SERVICES:
        logger.warning(f"Service {service} not found")
        return jsonify({"error": "Service not found"}), 404
    
    data = request.json
    try:
        response = requests.post(SERVICES[service], json=data, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling {service}: {str(e)}")
        return jsonify({"error": "Service unavailable"}), 503

    logger.info(f"Successfully routed request to {service}")
    return response.json(), response.status_code