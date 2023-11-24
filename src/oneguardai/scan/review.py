#!/usr/bin/env python3

"""
review.py: TODO: Headline...

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
from urllib.parse import urlparse
import subprocess

import requests
from bs4 import BeautifulSoup
from importlib import import_module
import http.client
from urllib.parse import quote

from oneguardai import const

# Child logger.
LOGGER = logging.getLogger(__name__)


def virustotal(domain: str) -> dict or None:
    """
    Get the virustotal report for the specified domain.
    """

    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    # TODO: Move API-key to environment variable.
    headers = {
            "accept": "application/json",
            "x-apikey":
                "bbf5ddd66e27f07672fe611a9235961751c7e3b59d57d478231315b29b155b59",
            }
    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            LOGGER.error("Could not fetch virustotal rating. Response status "
                         f"code: {response.status_code}."
                         )
            return None

        response = response.json()

        # Extract popularity and security stats from virustotal
        # api response.
        results = {"popularity": {key: item["rank"] for key, item in
                                  response["data"]["attributes"][
                                      "popularity_ranks"].items()},
                   "security": response["data"]["attributes"][
                       "last_analysis_stats"]
                   }

        return results

    except Exception as e:
        LOGGER.error("An error occurred while fetching the virustotal rating:"
                     f" {str(e)}."
                     )
        return None


def scamadviser(domain: str) -> dict or None:
    """
    Get the scamadviser score and more data for the specified domain.
    """

    url = f"https://www.scamadviser.com/check-website/{domain}"

    try:

        response = requests.get(url)

        if response.status_code != 200:
            LOGGER.error("Could not fetch scamadviser rating. Response status "
                         f"code: {response.status_code}."
                         )
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Scamadviser rating score.
        trustscore_div = soup.find("div", {"id": "trustscore"})
        if trustscore_div:
            trustscore_value = int(trustscore_div["data-rating"])
        else:
            trustscore_value = None

        # Backlinks are how many other sites link to specified domain.
        backlinks_div = soup.find("div", {"class": "block__col"},
                                  string="Backlinks"
                                  )
        if backlinks_div:
            backlinks_value = backlinks_div.find_next("div", {
                    "class": "block__col"
                    }
                                                      )
            backlinks_value = int(backlinks_value.string.strip())
        else:
            backlinks_value = None

        # Speed of the website loading.
        website_speed_div = soup.find("div", {"class": "block__col"},
                                      string="Website Speed"
                                      )
        if website_speed_div:
            website_speed_value = website_speed_div.find_next("div", {
                    "class": "block__col"
                    }
                                                              )
            website_speed_value = website_speed_value.string.strip()
        else:
            website_speed_value = None

        # SSL certificate validation.
        ssl_cert_div = soup.find("div", {"class": "block__col"},
                                 string="SSL certificate valid"
                                 )
        if ssl_cert_div:
            ssl_cert_value = ssl_cert_div.find_next("div", {
                    "class": "block__col"
                    }
                                                    )
            if ssl_cert_value.string.strip() == "valid":
                ssl_cert_value = True
            else:
                ssl_cert_value = False

        else:
            ssl_cert_value = None

        results = {"rating": trustscore_value,
                   "backlinks": backlinks_value,
                   "website_speed": website_speed_value,
                   "ssl_certificate_valid": ssl_cert_value,
                   }

        return results

    except Exception as e:
        LOGGER.error("An error occurred while fetching the scamadviser rating:"
                     f" {str(e)}."
                     )
        return None


def trustpilot(domain: str) -> dict[float, int] or None:
    """
    Get the trustpilot reviews for the specified domain.

    We need to scrape the website because TrustPilot does only provide
    a paid API (200 USD per month).
    """

    url = f"https://trustpilot.com/review/{domain}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            LOGGER.error("Could not fetch trustpilot rating. Response status "
                         f"code: {response.status_code}."
                         )
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        rating_element = soup.find(
                class_="typography_body-l__KUYFJ "
                       "typography_appearance-subtle__8_H2l"
                )

        rating_count = soup.find(
                class_="typography_body-l__KUYFJ "
                       "typography_appearance-default__AAY17"
                )

        # Convert strings to floats.
        if rating_element and rating_count:
            total_rating = rating_element.text.strip()
            total_rating = float(total_rating)

            total_count = rating_count.text.strip()
            total_count = total_count.replace("total", "").strip()
            total_count = total_count.replace(",", "").strip()
            total_count = int(total_count)

            return {"rating": total_rating, "review_count": total_count}

        else:
            return None

    except Exception as e:
        LOGGER.error("An error occurred while fetching the trustpilot rating:"
                     f" {str(e)}."
                     )
        return None


def getsafeonline(domain: str) -> dict or None:
    """
    Get the getsafeonline check for the specified domain.
    """

    url = f"https://check.getsafeonline.org/check/{domain}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            LOGGER.error("Could not fetch getsafeonline rating. Response "
                         f"status code: {response.status_code}."
                         )
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        results = {}

        review_sections = soup.find_all('div',
                                        class_='flex flex-col gap-4 '
                                               'md:flex-row'
                                        )

        for section in review_sections:
            a_element = section.find("a", class_="text-black")
            if a_element:
                source_name = a_element.text.strip()[: -1]

            img_element = section.find("img")
            if img_element:
                
                alt_text = img_element.get("alt", "").lower()

                if alt_text == "source-positive":
                    results[source_name] = True

                elif alt_text == "source-negative":
                    results[source_name] = False

                else:
                    results[source_name] = None

        return results

    except Exception as e:
        LOGGER.error("An error occurred while fetching the getsafeonline "
                     f"checks: {str(e)}."
                     )
        return None


# TODO: Move somewhere else!
def bypass_cloudflare(url: str) -> BeautifulSoup or None:
    encoded_url = quote(url, safe="")

    conn = http.client.HTTPSConnection("api.scrapingant.com")

    # Only 10000 requests per month are included in free plan.
    conn.request(
            "GET",
            f"/v2/general?url="
            f"{encoded_url}&x-api-key=2c4715421129452da7154a880ef35a14"
            f"&return_page_source=true"
            )

    res = conn.getresponse()
    data = res.read()

    html = data.decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    return soup


# WiP: not working yet!
def get_redirected_url(review_url, url_to_check):
    # review_url -> get the csrf token of search input field.
    soup = bypass_cloudflare(review_url)

    # response = requests.get(review_url)
    # soup = BeautifulSoup(response.text, 'html.parser')

    csrf_token = soup.find('input', {'name': '_csrf-frontend'}).get('value')

    search_url = 'https://www.scamdoc.com/interrogation'

    post_data = {
            '_csrf-frontend': csrf_token,
            'expression': url_to_check
            }

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36',
            }

    response = requests.post(search_url, data=post_data, headers=headers,
                             allow_redirects=False
                             )

    if response.status_code == 302:  # Forwards to the result page.
        redirected_url = response.headers['Location']
        return redirected_url
    else:
        redirected_url = response.headers['Location']
        return (f"URL nicht gefunden oder nicht bewertet auf ScamAdvisor. "
                f"{redirected_url}")


def social(domain: str) -> dict or None:
    """
    Get the social media profiles for the specified domain.
    """

    # Search for profiles with url.tld and url (shop.com and shop).
    domain_strip = '.'.join(domain.split('.')[:-1])

    # Need to import social-analyzer dynamically because it has a
    # '-' in its name.
    social_analyzer = import_module("social-analyzer").SocialAnalyzer()

    results = {"all_count": 0, "social_count": 0, "all": [], "social": []}
    for name in [domain, domain_strip]:
        result = social_analyzer.run_as_object(username=name, top=30,
                                               silent=True, output="json",
                                               filter="good", metadata=False,
                                               timeout=2, profiles="detected",
                                               trim=True, method="find",
                                               extract=False, options="link, "
                                                                      "type",
                                               )["detected"]

        for item in result:

            # 'https://my.shop.com/buy/this' -> 'shop'.
            domain_name = urlparse(item["link"]).netloc.split('.')[-2]

            # Save pretty name of social media platform and count.
            if domain_name not in results["all"]:
                results["all_count"] += 1

                results["all"].append(domain_name)

                if "Social" in item["type"]:
                    results["social"].append(domain_name)
                    results["social_count"] += 1

    return results


def social2(domain: str) -> dict or None:
    domain_strip = '.'.join(domain.split('.')[:-1])

    sherlock_local_path = f"{const.APP_PATH}/utils/sherlock/sherlock.py"
    opt_arguments = "--no-color"
    timeout_arg = "--timeout"
    timeout_val = "20"
    output_arg = "--output"
    output_val = ""

    results = {"social_count": 0, "social": []}

    try:
        result = subprocess.run(["python3", sherlock_local_path,
                                 domain_strip, opt_arguments, timeout_arg,
                                 timeout_val, output_arg, output_val],
                                capture_output=True,
                                text=True, check=True, timeout=300
                                )

        # print(result.stdout)

        # Regular expression (only name of social media platform).
        pattern = re.compile(r"\[\+\] (\w+):")

        matches = pattern.findall(result.stdout)

        for match in matches:
            results["social_count"] += 1

            results["social"].append(match)

        return results

    except subprocess.CalledProcessError as e:
        LOGGER.error("An error occurred while fetching the social media "
                     f"profiles: {str(e)} {str(e.output)}."
                     )
        return None


if __name__ == "__main__":
    # Find social media profiles (takes a 30-60 seconds).
    # soc = social("chicladdy.com")
    # if soc:
    #     print("Social:", soc)

    soc2 = social2("chicladdy.com")
    if soc2:
        print("Social2:", soc2)

    # trust = trustpilot("chicladdy.com")
    # if trust:
    #     print("Trustpilot:", trust)
    #
    # scam = scamadviser("chicladdy.com")
    # if scam:
    #     print("Scamadviser:", scam)
    #
    # virus = virustotal("chicladdy.com")
    # if virus:
    #     print("Virustotal:", virus)

    getsafe = getsafeonline("chicladdy.com")
    if getsafe:
        print("Getsafeonline:", getsafe)
