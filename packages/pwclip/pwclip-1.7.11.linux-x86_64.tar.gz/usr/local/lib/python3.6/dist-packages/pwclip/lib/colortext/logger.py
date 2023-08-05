#!/usr/bin/env python3

import sys
import logging
#from rainbow_logging_handler import RainbowLoggingHandler
"""
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

And to use it, create your own Logger:

# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return


logging.setLoggerClass(ColoredLogger)
"""




def logger(name, lvl='info'):
#	# 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
#	lvls = {
#      'debug': logging.DEBUG,
#      'info': logging.INFO,
#      'warning': logging.WARNING,
#      'error': logging.ERROR,
#      'critical': logging.CRITICAL}
#	_logger = logging.getLogger(name)
#	_logger.setLevel(lvl if lvl in lvls.values() else lvls[lvl])
#	formats = logging.Formatter("[%(asctime)-19s]%(lineno)-6d:%(filename)s%(module)s:%(funcName)s: %(message)s")  # same as default
#	handler = logging.FileHandler(name)
#	_logging.basicConfig
#	handler.setFormatter(formats)
#	_logger.addHandler(handler)
	logging.basicConfig(format='[%(asctime)-19s]%(lineno)-6d:%(filename)s%(module)s:%(funcName)s: %(message)s', datefmt='%F.%T')
	return logging
