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


def fetch_shopauskunft_domains():
    fetched_websites = []

    shopauskunft_categories = ["hardware", "software", "spielwaren",
                               "telekommunikation",
                               "unterhaltungs-elektronik", "foto-optik",
                               "haushalt", "sport-freizeit",
                               "bauen-heimwerken", "bueroartikel",
                               "bekleidung", "musik", "gesundheit",
                               "buecher", "sonstiges", "dvd_video",
                               "tiere", "garten-landwirtschaft",
                               "auto-motorrad", "essen-trinken",
                               "fluege-reisen", "schmuck",
                               "koerperpflege-kosmetik", "moebel",
                               "familie-kinder", "uhren", "schuhe",
                               "accessoires"]

    url = "https://www.shopauskunft.de"

    for category in shopauskunft_categories:

        print("---" * 20)
        print(f"Fetching all entries of category: {category} ..."
              )
        print("Fetched domains so far:", len(fetched_websites))

        page = 1
        while True:
            page_url = (f"{url}/{category}/?&eFOC[shoplist]["
                        f"sort]=issuetotal_down&eFOC[shoplist][pg]="
                        f"{page}#list")

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
                site_items = soup.find_all('tr',
                                           class_='erate-list-item'
                                           )

                if not site_items:
                    break  # Keine weiteren Einträge auf der Seite

                for site_item in site_items:

                    try:
                        # Shop link.
                        link = site_item.find('a', class_='subject-link')[
                            'href']
                        link = link.replace(
                                "https://www.shopauskunft.de/review/", ""
                                )

                        # Shop rating.
                        rating = site_item.find('td',
                                                class_='data-field '
                                                       'erate-satisfaction'
                                                ).text[:-1]
                        rating = float(rating.replace(",", "."))

                        # Shop rating count.
                        rating_count = int(site_item.find('td',
                                                          class_='counter '
                                                                 'total'
                                                          ).text
                                           )

                    except Exception:
                        continue

                    # Skip if rating is below 70% or less than 25 ratings.
                    if rating < 70 or rating_count < 25:
                        print(f"Skipped entry: {link} ({rating}%, "
                              f"{rating_count})"
                              )
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
    results = fetch_shopauskunft_domains()

    output_name = f'shopauskunft_all_categories'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
