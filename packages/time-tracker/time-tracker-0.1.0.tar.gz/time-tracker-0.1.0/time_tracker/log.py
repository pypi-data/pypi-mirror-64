import logging
from datetime import datetime
from dotenv import load_dotenv
import os


class Logger:
    def __init__(self):
        # Load envs
        load_dotenv()

        # Create missing directories
        if not os.path.exists("logs"):
            os.makedirs("logs")

        FORMAT = "%(asctime)-10s | %(levelname)s | %(message)s"

        if os.getenv("ENV") == "dev":
            logging.basicConfig(
                format=FORMAT, level=logging.INFO, handlers=[logging.StreamHandler()]
            )
        else:
            log_file = "logs/" + (datetime.today()).strftime("%Y-%m-%d") + ".log"
            logging.basicConfig(filename=log_file, format=FORMAT, level=logging.INFO)
