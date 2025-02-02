from flask import Blueprint, request, jsonify
from service.logger import logger
from service.config import SERVICE_NAME

import os
from PIL import Image
import numpy as np

import config

bp = Blueprint('service', __name__)

@bp.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        result = {"service": SERVICE_NAME, "output": data.get("input", "").upper()}

        print(os.listdir())
        print(config.DATA_DIR)

        img = Image.open(os.path.join(config.DATA_DIR, 'sample.jpeg'))
        np.savez_compressed(os.path.join(config.DATA_DIR, 'sample.npz'), arr=np.array(img))

        logger.info(f"Processed request: {data}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500