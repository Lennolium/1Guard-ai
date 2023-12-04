#!/usr/bin/env python3

"""
misc.py: TODO: Headline...

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
import logging
import re

import requests
from bs4 import BeautifulSoup

from oneguardai import const

# Child logger.
LOGGER = logging.getLogger(__name__)


def get_favicon(domain: str, soup: BeautifulSoup) -> str or None:
    """
    The get_favicon function takes in a domain and BeautifulSoup object
    as parameters. It then searches the BeautifulSoup object for any
    'link' tags with an attribute of 'rel' that matches either 'shortcut
    icon' or 'icon'. If it finds one, it returns the value of its 'href'
    attribute. If not, it attempts to make a GET request to
    https://{domain}/favicon.ico and return that if successful.

    :param domain: str: Specify the domain of the website
    :param soup: BeautifulSoup: Pass the beautifulsoup object
    :return: The favicon url of the website
    """

    for item in soup.find_all("link", attrs={
            "rel": re.compile("^(shortcut icon|icon)$", re.I)
            }
                              ):
        return item.get("href")

    try:
        testing = requests.get(f"https://{domain}/favicon.ico",
                               timeout=const.TIMEOUT
                               )
        if testing.status_code == 200:
            return f"{domain}/favicon.ico"

    except:
        return None


def favicon_external(domain: str, soup: BeautifulSoup) -> bool or None:
    """
    This function checks if the favicon is loaded from an external
    domain. This is a sign of phishing.

    :param soup: BeautifulSoup: Pass the beautifulsoup object
    :param domain: str: Specify the domain to be checked
    :return: True if the favicon is loaded from an external domain
    """

    favicon = get_favicon(domain, soup)

    # No favicon found.
    if favicon is None:
        return None

    # google --> google.com/favicon.ico
    elif favicon.rfind("/") >= 1 and "http" not in favicon:
        return False

    # https://example.com/favicon.ico
    elif domain in favicon:
        return False

    # popa.com --> https://static.parastorage.com/client/pfavico.ico
    # fb.com --> https://static.xx.fbcdn.net/rsrc.php/yv/r/B8BxsscfVBr.ico
    elif favicon.startswith("http") and domain not in favicon:
        return True

    else:
        return None


def website_traffic(response: requests.Response) -> int or None:
    """
    The website_traffic function takes in a requests.Response object and
    returns the number of bytes in the response content as an integer or
    None if there is no content.

    :param response: requests.Response: Pass in the response object
    :return: The length/size of the response content in bytes
    """
    try:
        traffic = int(len(response.content))
        return traffic

    except:
        return None


def forwarding(response: requests.Response) -> bool:
    """
    The function takes in a domain name as an argument
    and returns True if the domain is forwarding the user more than
    once. Scammers often use forwarding to hide the original domain
    name.

    :param response: requests.Response: Pass in the response object
    :return: True if the domain is not forwarding
    """

    if len(response.history) >= 1:
        return False

    else:
        return True
