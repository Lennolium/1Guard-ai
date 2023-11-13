#!/usr/bin/env python3

"""
const.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__build__ = "2023.1"
__date__ = "2023-11-07"
__status__ = "Prototype"

# Imports.
import configparser
import os
import platform

# Constants.
CURRENT_PLATFORM = platform.uname()[0].upper()  # 'DARWIN' / 'LINUX' ...
APP_PATH = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
USER_HOME = os.path.expanduser("~")
LOG_FILE = f"{APP_PATH}/trace.log"

# Configuration.
CONFIG_FILE = f"{APP_PATH}/config.ini"
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FILE, encoding="utf-8")
