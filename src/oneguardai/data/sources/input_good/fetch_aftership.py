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


def fetch_aftership_domains():
    fetched_websites = []

    url = "https://www.aftership.com"

    print("---" * 20)
    print(f"Fetching all entries from all categories ...")
    print("Fetched domains so far:", len(fetched_websites))

    page = 1
    while True:
        page_url = f"{url}/brands/page/{page}?sort=rank"

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
            site_items = soup.find_all('div',
                                       class_='rt-Grid rt-r-ai-center'
                                       )

            if not site_items:
                break  # Keine weiteren Einträge auf der Seite

            for site_item in site_items:

                try:
                    # Shop link.
                    link = site_item.find('a')["href"]
                    link = link.replace(
                            "https://www.aftership.com/brands/", ""
                            )


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

            print(f"Page {page} finished. Fetched domains so far:",
                  len(fetched_websites)
                  )
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
    results = fetch_aftership_domains()

    output_name = f'aftership_all_categories'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
