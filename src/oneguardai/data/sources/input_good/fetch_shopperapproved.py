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

import time

# Imports.
import requests
from bs4 import BeautifulSoup
import validators


def fetch_shopperapproved_domains():
    fetched_websites = []

    shopperapproved_categories = ["art", "clothes-accessories",
                                  "tools-supplies", "electronics",
                                  "entertainment", "food-beverages",
                                  "health-wellbeing", "product-services",
                                  "home-garden", "leisure", "sports",
                                  "transportation", ]

    url = "https://www.shopperapproved.com/directory"

    for category in shopperapproved_categories:

        print("---" * 20)
        print(f"Fetching all entries of category: {category} ..."
              )
        print("Fetched domains so far:", len(fetched_websites))

        page = 1
        while True:
            page_url = f"{url}/{category}?page={page}"

            for i in [0, 5, 10, 30, 60]:
                try:
                    response = requests.get(page_url, timeout=(i + 5))
                    break
                except Exception:
                    time.sleep(i)
                    continue

            if response is None:
                print(
                        f"Error fetching page {page}. Final try. "
                        f"Skipping page."
                        )
                page += 1
                continue

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                site_items = soup.find_all('h4', class_='f18')

                if not site_items:
                    break  # Keine weiteren Einträge auf der Seite

                for site_item in site_items:

                    try:
                        link = site_item.find('a')['href']
                    except Exception:
                        continue

                    # Check if shop name is a valid domain format.
                    if validators.domain(link):
                        if "www." in link:
                            link = link.replace("www.", "")

                        if "https://" in link:
                            link = link.replace("https://", "")

                        if "http://" in link:
                            link = link.replace("http://", "")

                    else:
                        if "www." in link:
                            link = link.replace('www.', '')

                        if "https://" in link:
                            link = link.replace('https://', '')

                        if "http://" in link:
                            link = link.replace('http://', '')

                        if "/" in link:
                            link = link.split("/")[0]

                    if link is not None:
                        if not link == "":
                            if link not in fetched_websites:
                                if validators.domain(link):
                                    print("Added entry:", link)
                                    fetched_websites.append(link)

                page += 1
            else:
                print("All entries fetched.")
                break

    return fetched_websites


def write_to_txt(websites, output_file):
    with open(f"{output_file}.txt", 'w') as file:
        for website in websites:
            file.write(website + '\n')


# Check how many lines are in the file
def length(file_out):
    with open(f'{file_out}.txt') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == '__main__':
    results = fetch_shopperapproved_domains()

    output_name = f'shopperapproved_all_categories'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
