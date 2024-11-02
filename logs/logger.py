"""
This module configures the logging for the application.

Logging Configuration:
- The logging format includes the timestamp, logger name, log level, and message.
- The logging level is set to DEBUG, allowing all messages at this level and above to be captured.

Usage:
This logger can be imported and used throughout the application to log messages for 
debugging and tracking the application's behavior.
"""


from logging import getLogger, DEBUG
import logging

FORMAT = "%(asctime)s : %(name)s : %(levelname)s : %(message)s"
logging.basicConfig(format=FORMAT, level=DEBUG)

logger = getLogger()