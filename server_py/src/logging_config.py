import logging
import os
from datetime import datetime

def setup_logging(debug_mode: bool):
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

    # Clear existing handlers to prevent duplicate logs
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if debug_mode:
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)s %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode='a'),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=logging.CRITICAL)  # Suppress all logs
        logging.disable(logging.CRITICAL)

    # Set specific logger for gemini-cli-mcp
    logger = logging.getLogger("gemini-cli-mcp")
    if debug_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL)

    return logger
