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
import requests
from bs4 import BeautifulSoup


def get_betruegerische_websites(url):
    betruegerische_websites = []

    page = 1
    while True:
        page_url = f"{url}?tx_solr%5Bpage%5D={page}"
        response = requests.get(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            site_items = soup.find_all('div', class_='site-item')

            if not site_items:
                break  # Keine weiteren Einträge auf der Seite

            for site_item in site_items:
                website_name = site_item.find('a', class_='site-item__link'
                                              ).get_text(strip=True)
                betruegerische_websites.append(website_name)

            page += 1
        else:
            print(
                    f"Fehler beim Abrufen der Seite {page_url}. Statuscode: "
                    f"{response.status_code}, Alle Seiten wurden abgerufen."
                    )
            break

    return betruegerische_websites


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
    # watchlist_url = ('https://www.watchlist-internet.at/liste
    # -betruegerischer-shops/')
    # output_name = 'betruegerische_websites'

    watchlist_url = ("https://www.watchlist-internet.at/liste-problematischer"
                     "-shops/")
    output_name = 'problematische_websites'

    betruegerische_websites = get_betruegerische_websites(watchlist_url

                                                          )
    write_to_txt(betruegerische_websites, output_name)

    print(
            f"{len(betruegerische_websites)} betrügerische Websites wurden "
            f"extrahiert und in betruegerische_websites.txt gespeichert."
            )

    length_domains = length(output_name)
    print(f"Die Datei enthält {length_domains} betrügerische Websites.")
