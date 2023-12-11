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


COUNTRY_MAP = {"NaN": "NaN", "AD": 0, "AE": 1, "AF": 2, "AG": 3, "AI": 4,
               "AL": 5, "AM": 6, "AN": 7, "AO": 8, "AQ": 9, "AR": 10, "AS": 11,
               "AT": 12, "AU": 13, "AW": 14, "AX": 15, "AZ": 16, "BA": 17,
               "BB": 18, "BD": 19, "BE": 20, "BF": 21, "BG": 22, "BH": 23,
               "BI": 24, "BJ": 25, "BL": 26, "BM": 27, "BN": 28, "BO": 29,
               "BR": 30, "BS": 31, "BT": 32, "BV": 33, "BW": 34, "BY": 35,
               "BZ": 36, "CA": 37, "CC": 38, "CD": 39, "CF": 40, "CG": 41,
               "CH": 42, "CI": 43, "CK": 44, "CL": 45, "CM": 46, "CN": 47,
               "CO": 48, "CR": 49, "CU": 50, "CV": 51, "CX": 52, "CY": 53,
               "CZ": 54, "DE": 55, "DJ": 56, "DK": 57, "DM": 58, "DO": 59,
               "DZ": 60, "EC": 61, "EE": 62, "EG": 63, "EH": 64, "ER": 65,
               "ES": 66, "ET": 67, "FI": 68, "FJ": 69, "FK": 70, "FM": 71,
               "FO": 72, "FR": 73, "GA": 74, "GB": 75, "GD": 76, "GE": 77,
               "GF": 78, "GG": 79, "GH": 80, "GI": 81, "GL": 82, "GM": 83,
               "GN": 84, "GP": 85, "GQ": 86, "GR": 87, "GS": 88, "GT": 89,
               "GU": 90, "GW": 91, "GY": 92, "HK": 93, "HM": 94, "HN": 95,
               "HR": 96, "HT": 97, "HU": 98, "ID": 99, "IE": 100, "IL": 101,
               "IM": 102, "IN": 103, "IO": 104, "IQ": 105, "IR": 106,
               "IS": 107, "IT": 108, "JE": 109, "JM": 110, "JO": 111,
               "JP": 112, "KE": 113, "KG": 114, "KH": 115, "KI": 116,
               "KM": 117, "KN": 118, "KP": 119, "KR": 120, "KW": 121,
               "KY": 122, "KZ": 123, "LA": 124, "LB": 125, "LC": 126,
               "LI": 127, "LK": 128, "LR": 129, "LS": 130, "LT": 131,
               "LU": 132, "LV": 133, "LY": 134, "MA": 135, "MC": 136,
               "MD": 137, "ME": 138, "MF": 139, "MG": 140, "MH": 141,
               "MK": 142, "ML": 143, "MM": 144, "MN": 145, "MO": 146,
               "MP": 147, "MQ": 148, "MR": 149, "MS": 150, "MT": 151,
               "MU": 152, "MV": 153, "MW": 154, "MX": 155, "MY": 156,
               "MZ": 157, "NA": 158, "NC": 159, "NE": 160, "NF": 161,
               "NG": 162, "NI": 163, "NL": 164, "NO": 165, "NP": 166,
               "NR": 167, "NU": 168, "NZ": 169, "OM": 170, "PA": 171,
               "PE": 172, "PF": 173, "PG": 174, "PH": 175, "PK": 176,
               "PL": 177, "PM": 178, "PN": 179, "PR": 180, "PS": 181,
               "PT": 182, "PW": 183, "PY": 184, "QA": 185, "RE": 186,
               "RO": 187, "RS": 188, "RU": 189, "RW": 190, "SA": 191,
               "SB": 192, "SC": 193, "SD": 194, "SE": 195, "SG": 196,
               "SH": 197, "SI": 198, "SJ": 199, "SK": 200, "SL": 201,
               "SM": 202, "SN": 203, "SO": 204, "SR": 205, "ST": 206,
               "SV": 207, "SY": 208, "SZ": 209, "TC": 210, "TD": 211,
               "TF": 212, "TG": 213, "TH": 214, "TJ": 215, "TK": 216,
               "TL": 217, "TM": 218, "TN": 219, "TO": 220, "TR": 221,
               "TT": 222, "TV": 223, "TW": 224, "TZ": 225, "UA": 226,
               "UG": 227, "UM": 228, "US": 229, "UY": 230, "UZ": 231,
               "VA": 232, "VC": 233, "VE": 234, "VG": 235, "VI": 236,
               "VN": 237, "VU": 238, "WF": 239, "WS": 240, "YE": 241,
               "YT": 242, "ZA": 243, "ZM": 244, "ZW": 245
               }

VELOCITY_MAP = {"NaN": "NaN", "Very Slow": 0, "Slow": 1,
                "Average": 2, "Fast": 3, "Very Fast": 4,
                }
