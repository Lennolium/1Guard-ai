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
import re

# Constants.
CURRENT_PLATFORM = platform.uname()[0].upper()  # 'DARWIN' / 'LINUX' ...
APP_PATH = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
USER_HOME = os.path.expanduser("~")
LOG_FILE = f"{APP_PATH}/trace.log"

# Configuration.
CONFIG_FILE = f"{APP_PATH}/config.ini"
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FILE, encoding="utf-8")

# RegEx.
SHORTENING_RE = re.compile(
        r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co"
        r"|tinyurl|tr\.im|is\.gd|cli\.gs|"
        r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr"
        r"|twurl\.nl|snipurl\.com|"
        r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com"
        r"|snipr\.com|fic\.kr|loopt\.us|"
        r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly"
        r"|bit\.do|lnkd\.in|"
        r"db\.tt|qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com"
        r"|ity\.im|"
        r"q\.gs|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl"
        r"\.com|cutt\.us|u\.bb|yourls\.org|"
        r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl"
        r"\.com|qr\.net|1url\.com|tweez\.me|v\.gd|link"
        r"\.zip\.net"
        )
MOUSEOVER_RE = re.compile(r"<script>.+onmouseover.+</script>")
RIGHT_CLICK_RE = re.compile(r"event.button ?== ?2")
POPUP_RE = re.compile(r"alert\(")
I_FRAME_RE = re.compile(r"[<iframe>|<frameBorder>]")

# Scraping settings.
INIT_TIMEOUT = 15
CF_TIMEOUT = 30
TIMEOUT = 10

# Proxy settings.
# free_proxy = FreeProxy(country_id=["DE", "AT", "CH", "NL"], timeout=1).get()
#
# print(free_proxy)
# PROXYS = {"http": free_proxy}

# API settings and keys. TODO: change to env variables!
API_KEY_VT = ""
API_KEY_PR = ""
API_KEY_SCRAPANT = ""
