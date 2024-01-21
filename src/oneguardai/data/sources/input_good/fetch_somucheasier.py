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


def fetch_somucheasier_domains():
    fetched_websites = []

    somucheasier_categories = ["books", "catalogue-shops",
                               "womens-clothing", "womens-shoes", "lingerie",
                               "childrens-clothing", "sports-clothing",
                               "clothes-catalogues", "jewellery-shops-uk",
                               "designer-handbags", "mens-clothing",
                               "mens-shoes", "designer-clothing",
                               "schoolwear-uk-school-clothing",
                               "outdoor-clothing", "maternity-clothing",
                               "designer-sunglasses", "computers",
                               "department-stores", "dvds-videos",
                               "electrical-goods", "supermarkets-uk",
                               "food-hampers", "wines-and-champagne",
                               "beer-and-spirits", "gourmet-food",
                               "organic-food", "furniture-stores-uk",
                               "gifts-for-women", "unusual-gifts",
                               "gift-baskets-and-hampers",
                               "high-street-vouchers", "gift-finders",
                               "gifts-for-men", "flowers", "greeting-cards",
                               "online-gift-certificates",
                               "beauty-products", "health-care-products",
                               "male-grooming", "perfume-shops",
                               "diet-and-fitness", "department-stores",
                               "home-furnishings", "furniture-stores-uk",
                               "gardening-shops-uk", "buy-a-garden-shed",
                               "catalogue-shops", "homeware",
                               "diy-stores-uk", "buy-garden-furniture",
                               "mobile-phone-shops", "motoring",
                               "music-cds", "pet-shops",
                               "sports-and-leisure", "accommodation",
                               "travel-accessories"]

    url = "https://www.somucheasier.co.uk"

    for category in somucheasier_categories:

        print("---" * 20)
        print(f"Fetching all entries of category: {category} ..."
              )
        print("Fetched domains so far:", len(fetched_websites))

        page_url = f"{url}/{category}.html"

        for i in [0, 5, 10, 30, 60]:
            try:
                response = requests.get(page_url, timeout=(i + 5))
                break
            except Exception:
                time.sleep(i)
                continue

        if response is None:
            print(
                    f"Error fetching page. Final try. "
                    f"Skipping page."
                    )
            continue

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            site_items = soup.find_all('a', class_='linkblue')

            real_site_items = []

            for site in site_items:
                if site.text == "Click here":
                    real_site_items.append(site)

            if not real_site_items:
                break  # Keine weiteren Einträge auf der Seite

            for site_item in real_site_items:

                try:
                    # Shop link.
                    link = site_item['href']

                    if ("www.awin" in link or "awin.com" in link or
                            "www.webgains.com" in link):
                        try:
                            response_awin = requests.get(link,
                                                         allow_redirects=True,
                                                         timeout=5
                                                         )
                            link = response_awin.url

                        except Exception:
                            continue

                        if "webgains.com" in link or "awin.com" in link:
                            continue


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

                    if "www" in link:
                        www = link.split(".")[0]
                        link = link.replace(f"{www}.", "")

                    if "?" in link:
                        link = link.split("?")[0]

                    if link.startswith("affiliate"):
                        aff_split = link.split(".")[0]
                        link = link.replace(f"{aff_split}.", "")

                if link is not None:
                    if not link == "":
                        if link not in fetched_websites:
                            if validators.domain(link):
                                print("Added entry:", link)
                                fetched_websites.append(link)

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
    results = fetch_somucheasier_domains()

    output_name = f'somucheasier_all_categories'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
