from flask import Blueprint, request, jsonify
from service.logger import logger
from service.config import SERVICE_NAME

bp = Blueprint('service', __name__)

@bp.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        result = {"service": SERVICE_NAME, "output": data.get("input", "").upper()}
        logger.info(f"Processed request: {data}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500