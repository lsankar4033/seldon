import logging
import time

from archivist.db import Database
from archivist.w3 import W3

LOOP_WAIT_SECS = 60

logger = logging.getLogger('archivist')


def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')


if __name__ == '__main__':
    configure_logging()

    db = Database()
    w3 = W3()

    scraper_loop(db, w3)
