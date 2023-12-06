#!/usr/bin/env python3

"""
registrar.py: TODO: Headline...

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
from datetime import date, datetime

import country_converter
import whois

# Child logger.
LOGGER = logging.getLogger(__name__)


def whois_info(domain: str) -> dict:
    try:
        whois_full = whois.whois(domain)

        # Early exit if WHOIS info is not available.
        if whois_full is None:
            return {}

        # Check how old the domain is.
        whois_creation = whois_full["creation_date"]
        if isinstance(whois_creation, list):
            creation_date = whois_full["creation_date"][0]
        else:
            creation_date = whois_full["creation_date"]

        created_months = int((datetime.now() - creation_date).days / 30)

        # Check when the domain was last updated.
        whois_updated = whois_full["updated_date"]
        if isinstance(whois_updated, list):
            updated_date = whois_full["updated_date"][0]
        else:
            updated_date = whois_full["updated_date"]

        updated_months = int((datetime.now() - updated_date).days / 30)

        # Check when the domain expires.
        whois_expiration = whois_full["expiration_date"]
        if isinstance(whois_expiration, list):
            expiration_date = whois_full["expiration_date"][0]
        else:
            expiration_date = whois_full["expiration_date"]

        expires_months = int((expiration_date - datetime.now()).days / 30)

        # Check if domain is using DNSSEC.
        if whois_full["dnssec"] == "unsigned":
            dnssec = False

        elif isinstance(whois_full["dnssec"], list):
            dnssec = whois_full["dnssec"][0]
            if dnssec == "unsigned":
                dnssec = False
        else:
            dnssec = True

        # Get the country of the domain.
        country = whois_full["country"]

        # Convert country to ISO 3166-1 alpha-2 code if it not already.
        if len(country) != 2:
            country = country_converter.convert(names=country, to='ISO2',
                                                not_found="NaN"
                                                )

        # Check if domain privacy is enabled.
        privacy_names = ["private", "whoisguard", "privacy", "protected",
                         "redacted", "anonymized", "anonymised", "null",
                         "personal data", "personal information",
                         "applicable laws", "disclosed", "restricted", ]

        if isinstance(whois_full["name"], list):
            whois_name = whois_full["name"][0]
        elif whois_full["name"] is None:
            whois_name = "null"
        else:
            whois_name = whois_full["name"]

        if isinstance(whois_full["org"], list):
            whois_org = whois_full["org"][0]
        elif whois_full["org"] is None:
            whois_org = "null"
        else:
            whois_org = whois_full["org"]

        privacy = False
        for priv in privacy_names:
            if priv in whois_name.lower():
                privacy = True
                break

            elif priv in whois_org.lower():
                privacy = True
                break

        results = {"created_months": created_months,
                   "last_updated_months": updated_months,
                   "expires_in_months": expires_months,
                   "dnssec": dnssec,
                   "country": country,
                   "domain_privacy": privacy,
                   }

        return results

    except Exception as e:
        LOGGER.error(f"Could not fetch WHOIS info. Error: {str(e)},")
        return {}


if __name__ == "__main__":
    website_domain = "11trikots.com"
    whois_info = whois_info(website_domain)

    if whois_info:
        print(whois_info)
    else:
        print("WHOIS-Informationen nicht verfügbar.")
