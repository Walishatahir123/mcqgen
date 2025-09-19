# each n everything that be used in the project so it will be logged each n every thing
import logging
import os
from datetime import datetime

# Define log file name with timestamp
Log_File = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create logs directory
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

# Full log file path
LOG_FILEPATH = os.path.join(log_path, Log_File)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[%(asctime)s] [%(lineno)d] [%(name)s] - %(levelname)s - %(message)s"
)

# Example usage
logger = logging.getLogger(__name__)
logger.info("Logging system initialized successfully!")
