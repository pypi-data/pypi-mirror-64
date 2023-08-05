import logging
import sys
import os

logger = logging.getLogger(__name__)
ch = logging.StreamHandler(stream=sys.stderr)
ch.setLevel(os.getenv("LOG_LEVEL", "INFO"))

logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
logger.addHandler(ch)

def getLogger(name, toFile=False):
    logger = logging.getLogger(name)


    formatter = logging.Formatter('%(asctime)s - %(name)%s - %(levelname) -%(message)s')
    ch.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    ch.setFormatter(formatter)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    logger.addHandler(ch)
    if toFile:
        fileHandler = logging.FileHandler(f'/tmp/feed/logs/{name}.log')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

