from flask import Flask
from flask_cors import CORS
from gateway.routes import bp
from gateway.logger import logger
from gateway.config import GATEWAY_PORT

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all requests

app.register_blueprint(bp)

if __name__ == '__main__':
    logger.info(f"🚀 Starting Gateway API on port {GATEWAY_PORT}...")
    app.run(host='0.0.0.0', port=GATEWAY_PORT, debug=True)