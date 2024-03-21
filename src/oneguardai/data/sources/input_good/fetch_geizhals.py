#!/usr/bin/env python3

"""
fetch_watchlist.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-12-18"
__status__ = "Prototype/Development/Production"

# Imports.
import time
import random

import requests
from bs4 import BeautifulSoup
import validators

from oneguardai import const
from urllib.parse import quote


def bypass_toomuchrequests(url: str) -> requests.Response or None:
    encoded_url = quote(url, safe="")

    # WebScraper Alternatives: ScraperBox, SerpStack, WebScraping.AI
    endpoint = (f"https://api.scrapingant.com/v2/general?url="
                f"{encoded_url}&x-api-key="
                f"{const.API_KEY_SCRAPANT}&proxy_country=DE"
                f"&return_page_source=true")

    try:
        response = requests.get(endpoint, timeout=15,
                                allow_redirects=True
                                )

        if response.status_code != 200:
            print("Could not bypass protection. Response "
                  f"status code: {response.status_code}."
                  )
            return None

        return response

    except Exception as e:
        print(
                f"An error occurred while trying to bypass  "
                f"protection: {str(e)} ..."
                )

        return None


def fetch_geizhals_domains():
    fetched_websites = []

    url = "https://geizhals.de"

    print("---" * 20)
    print(f"Fetching all entries of geizhals ..."
          )

    page = 1
    while True:

        if page > 60:
            break

        print("---" * 20)
        print("Fetched domains so far:", len(fetched_websites))
        print(f"Fetching page {page} ...")

        page_url = f"{url}/?keywords=hlist&pg={page}"

        time.sleep(random.uniform(1, 5))
        try:
            response = requests.get(page_url, timeout=10)

        except Exception:
            print("Getting rate limited. Trying to bypass ...")
            response = bypass_toomuchrequests(page_url)

        if response.status_code == 429:
            print("Getting rate limited. Trying to bypass ...")
            response = bypass_toomuchrequests(page_url)

        if response is None:
            print(
                    f"Error fetching page {page}. Final try. "
                    f"Skipping page."
                    )
            page += 1
            continue

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            site_items = soup.find_all('div',
                                       class_='row'
                                       )

            if not site_items:
                break  # Keine weiteren Einträge auf der Seite

            for site_item in site_items:

                try:
                    # Shop link.
                    link = site_item.find('div', class_='cell').find('a').get(
                            'href'
                            )

                    link = f"https://geizhals.de/{link}"

                    # Shop rating.
                    rating = float(site_item.find('div',
                                                  class_='stars-rating-label'
                                                  ).text[:-1]
                                   )

                    # Shop rating count.
                    rating_count = site_item.find('div',
                                                  class_='stars-rating-label-bottom'
                                                  ).text
                    rating_count = int(rating_count.split(" ")[0])

                except Exception:
                    continue

                # Skip if rating is < 70% (3.5) or less than 10 ratings.
                if rating < 3.5 or rating_count < 10:
                    print(f"Skipped entry: {link} ({rating}, "
                          f"{rating_count})"
                          )
                    continue

                # Check if shop name is a valid domain format.
                if validators.url(link) and link is not None:
                    if link != "" and link not in fetched_websites:
                        print("Added entry:", link)
                        fetched_websites.append(link)

            page += 1
        else:
            print("All entries fetched.")
            break

    return fetched_websites


def post_process_gh():
    finished_domains = []
    max_retries = 5
    retry_counter = 0

    with open("geizhals_all_categories_raw.txt", 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    for line in lines:
        time.sleep(random.uniform(1, 5))
        try:
            response = requests.get(line, timeout=10)

        except Exception:
            if retry_counter > max_retries:
                print("Max retries reached. Skipping ...")
                break

            print("Getting rate limited. Trying to bypass ...")
            response = bypass_toomuchrequests(line)
            retry_counter += 1

        if response.status_code == 429:
            if retry_counter > max_retries:
                print("Max retries reached. Skipping ...")
                break

            print("Getting rate limited. Trying to bypass ...")
            response = bypass_toomuchrequests(line)
            retry_counter += 1

        if response is None:
            print(
                    f"Final try. "
                    f"Skipping page."
                    )
            continue

        if response.status_code == 200:
            if retry_counter > 0:
                retry_counter -= 1
            elif retry_counter <= 0:
                retry_counter = 0

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            contact_item = soup.find('div',
                                     class_='merchant-contact'
                                     )

            contact_links = contact_item.find_all('a')
            contact_email = contact_links[-1].get('href')

            website_url = contact_email.split('@')[-1]

            if validators.domain(website_url) and website_url != "":
                if website_url is not None:
                    if website_url not in finished_domains:
                        finished_domains.append(website_url)
                        print(f"Added entry:", website_url)


        except Exception as e:
            print("Error while parsing website url:", str(e))
            continue

    return finished_domains


def write_to_txt(websites, output_file):
    with open(f"{output_file}.txt", 'w') as file:
        for website in websites:
            file.write(website + '\n')


# Check how many lines are in the file
def length(file_out):
    with open(f'{file_out}.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    return len(lines)


if __name__ == '__main__':
    output_name = f'geizhals_all_categories_raw'
    output_name_final = f'geizhals_all_categories'

    # Gets us the links to the geizhals shop pages.
    results = fetch_geizhals_domains()
    write_to_txt(results, output_name)

    # Gets us the domains of the shops from the geizhals pages.
    results2 = post_process_gh()
    write_to_txt(results2, output_name_final)

    length_domains = length(output_name_final)
    print(f"The file {output_name_final}.txt has {length_domains} domains in "
          f"total."
          )
