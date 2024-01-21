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


def fetch_trustpilot_domains(country):
    fetched_websites = []
    trustpilot_categories = ['animals_pets', 'events_entertainment',
                             'home_garden', 'restaurants_bars',
                             'beauty_wellbeing',
                             'food_beverages_tobacco', 'home_services',
                             'shopping_fashion',
                             'business_services', 'health_medical',
                             'sports', 'construction_manufactoring',
                             'hobbies_crafts',
                             'media_publishing', 'public_local_services',
                             'electronics_technology',
                             'vehicles_transportation']
    if country == 'de':
        url = "https://www.trustpilot.de"
    else:
        url = "https://www.trustpilot.com"

    for category in trustpilot_categories:

        print(f"Fetching all entries with 4+ stars of category: {category} "
              f"..."
              )

        page = 1
        while True:
            if country == 'de' or country == 'us':
                page_url = (f"{url}/categories/{category}?page="
                            f"{page}&sort=reviews_count&trustscore=4.0")

            else:
                page_url = (f"{url}/categories/{category}?country="
                            f"{country.upper()}?page="
                            f"{page}&sort=reviews_count&trustscore=4.0")

            response = requests.get(page_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                site_items = soup.find_all('div', class_="paper_paper__1PY90 "
                                                         "paper_outline__lwsUX "
                                                         "card_card__lQWDv "
                                                         "card_noPadding__D8PcU "
                                                         "styles_wrapper__2JOo2"
                                           )

                if not site_items:
                    break  # Keine weiteren Einträge auf der Seite

                for site_item in site_items:
                    website_name = site_item.find('a')['href']

                    website_name = website_name.replace('/review/', '')

                    if "www." in website_name:
                        website_name = website_name.replace('www.', '')

                    if "https://" in website_name:
                        website_name = website_name.replace('https://', '')

                    if "http://" in website_name:
                        website_name = website_name.replace('http://', '')

                    if "/" in website_name:
                        website_name = website_name.split("/")[0]

                    fetched_websites.append(website_name)

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
    country = "au"  # "de" or "us" or "gb" ...
    results = fetch_trustpilot_domains(country)

    output_name = f'trustpilot_all_categories_{country}'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
