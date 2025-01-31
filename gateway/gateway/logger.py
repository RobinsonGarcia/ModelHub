import logging
import sys
from gateway.config import LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]  # ✅ Ensure logs go to stdout
)

logger = logging.getLogger(__name__)