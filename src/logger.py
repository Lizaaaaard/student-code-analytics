import logging
import time
from datetime import datetime
from pathlib import Path, os

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logger():
    now = time.time()
    for f in os.listdir(LOG_DIR):
        file_path = LOG_DIR / f
        if file_path.is_file() and file_path.stat().st_mtime < now - (3 * 86400):
            os.remove(file_path)

    log_file = LOG_DIR /f"{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO,
        handlers = [
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ])

    return logging.getLogger('StudentCodeAnalytics')


logger = setup_logger()