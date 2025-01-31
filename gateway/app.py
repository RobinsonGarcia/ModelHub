from flask import Flask
from gateway.routes import bp
from gateway.logger import logger

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    logger.info("Starting Gateway API...")
    app.run(host='0.0.0.0', port=5000)