from flask import Flask
from service.routes import bp
from service.logger import logger
from service.config import PORT, SERVICE_NAME

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    logger.info(f"Starting {SERVICE_NAME} on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT)