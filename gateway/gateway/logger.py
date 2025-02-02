import logging
import sys
import os
from gateway.config import LOG_LEVEL, DATA_DIR

# Define a log file path within the shared data folder
log_file = os.path.join(DATA_DIR, "gateway.log")

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)