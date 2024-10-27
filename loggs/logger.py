from logging import getLogger, DEBUG
import logging

FORMAT = "%(asctime)s : %(name)s : %(level)s : %(message)s"
logging.basicConfig(format=FORMAT, level=DEBUG)

logger = getLogger()