import logging
import sys
from service.config import LOG_LEVEL, SERVICE_NAME

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=f"%(asctime)s - {SERVICE_NAME} - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(SERVICE_NAME)