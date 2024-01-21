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
import validators


def fetch_trustedshops_domains(country, cert):
    fetched_websites = []

    if country == "de":
        trustedshops_categories = ["mobel_dekorationsartikel",
                                   "haushaltswaren_haushaltsgerate",
                                   "baumarkt",
                                   "hobby_sammeln_freizeitartikel",
                                   "geschenke",
                                   "bekleidung", "lebensmittel",
                                   "drogerieartikel_kosmetik",
                                   "buro_schule_beruf", "gartenbedarf",
                                   "sportartikel",
                                   "computer_unterhaltungselektronik_zubehor",
                                   "genussmittel", "spielwaren_baby_kind",
                                   "auto_motorrad_zubehor", "schmuck_uhren",
                                   "tierbedarf", "schuhe",
                                   "foto_druck_book_on_demand",
                                   "koffer_taschen_lederwaren", "bucher",
                                   "energie", "medikamente", "edelmetalle",
                                   "floristik", "karneval_kostume", "optiker",
                                   "consulting", "tickets", "musik_film",
                                   "reisen_hotels", "telekommunikation",
                                   "finanzen_versicherungen", ]

        url = "https://www.trustedshops.de/shops"

    else:
        url = "https://www.trustedshops.co.uk/shops"

        trustedshops_categories = ["furniture_decoration", "diy",
                                   "household_goods",
                                   "hobbys_collecting_freetime",
                                   "computers_electronics",
                                   "office_business_supplies", "clothing",
                                   "gifts", "food", "chemists_cosmetics",
                                   "sports_goods", "jewellery_watches",
                                   "photo_print_book_on_demand",
                                   "luggage_bags_leather_goods",
                                   "gardening_supplies",
                                   "toys_baby_children",
                                   "cars_motorbikes_accessories",
                                   "shoes", "pharmaceuticals",
                                   "luxury_foods_drinks_tobacco",
                                   "pet_supplies", "energy", "music_film",
                                   "books", "carnival_fancy_dress_costumes",
                                   "telecommunication", "travel_hotels",
                                   "consulting", "opticians",
                                   "precious_metals", "floristry",
                                   "finance_insurance", "tickets"]

    for category in trustedshops_categories:

        print("---" * 20)
        print(f"Fetching all entries with valid TrustedShops certificate of "
              f"category: {category} ..."
              )
        print("Fetched domains so far:", len(fetched_websites))

        page = 1
        while True:
            if cert:
                page_url = (f"{url}/{category}/?page="
                            f"{page}&sort=stars"
                            f"&hasValidCertificate=true")

            else:
                page_url = (f"{url}/{category}/?page="
                            f"{page}&sort=stars")

            response = requests.get(page_url, timeout=5)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                site_items = soup.find_all('a',
                                           class_='ShopResultItemstyles__Resul'
                                                  'tItem-sc-3gooul-0 dXCtjT'
                                           )

                if not site_items:
                    break  # Keine weiteren Einträge auf der Seite

                for site_item in site_items:
                    try:
                        shop_name = site_item.find('h3',
                                                   class_='CardHeaderstyles__Headi'
                                                          'ngName-sc-a4i44w-1'
                                                   ).text.strip()

                        shop_rating_count = site_item.find('span',
                                                           class_='ShopStatusstyle'
                                                                  's__RatingNumber'
                                                                  '-sc-9ta2lu-3'
                                                           )

                        # No ratings at all.
                        if shop_rating_count is None:
                            continue

                        else:
                            shop_rating_count = shop_rating_count.text.strip(
                                    ).split(" ")[0]

                        if "," in shop_rating_count:
                            shop_rating_count = shop_rating_count.replace(",",
                                                                          ""
                                                                          )

                        if "." in shop_rating_count:
                            shop_rating_count = shop_rating_count.replace(".",
                                                                          ""
                                                                          )

                        # Check if shop has at least 25 ratings.
                        if int(shop_rating_count) < 25:
                            continue

                        shop_rating = site_item.find('span',
                                                     class_='ShopStatusstyles__Rat'
                                                            'ingHeading-sc-9ta2'
                                                            'lu-1'
                                                     ).get_text().strip()

                        # No rating at all.
                        if shop_rating is None:
                            continue

                        # Check if shop has at least 4.0 rating.
                        if float(shop_rating) < 4.0:
                            continue

                        # Check if shop name is a valid domain format.
                        if validators.domain(shop_name):
                            if "www." in shop_name:
                                shop_name = shop_name.replace("www.", "")

                            if "https://" in shop_name:
                                shop_name = shop_name.replace("https://", "")

                            if "http://" in shop_name:
                                shop_name = shop_name.replace("http://", "")

                            if "//" in shop_name:
                                shop_name = shop_name.replace('//', '')

                            if "/" in shop_name:
                                shop_name = shop_name.split("/")[0]

                        else:
                            if "www." in shop_name:
                                shop_name = shop_name.replace('www.', '')

                            if "https://" in shop_name:
                                shop_name = shop_name.replace('https://', '')

                            if "http://" in shop_name:
                                shop_name = shop_name.replace('http://', '')

                            if "//" in shop_name:
                                shop_name = shop_name.replace('//', '')

                            if "/" in shop_name:
                                shop_name = shop_name.split("/")[0]

                            # Check again if format is valid now.
                            if not validators.domain(shop_name):
                                # If not we need to follow the link to the
                                # review site of the shop on TrustedShops.
                                ts_link = site_item['href']
                                response2 = requests.get(ts_link, timeout=5)

                                # If error, skip this entry.
                                if response2.status_code != 200:
                                    print("Error fetching entry. Skipping ...")
                                    continue

                                soup2 = BeautifulSoup(response2.text,
                                                      'html.parser'
                                                      )

                                link_element = soup2.find('a',
                                                          class_='Linkstyles__Link'
                                                                 'AsButton-sc-1h68'
                                                                 'u9x-1 '
                                                                 'sc-f6e403b'
                                                                 '3-2 gXpwGI '
                                                                 'kjrK'
                                                                 'NM'
                                                          )

                                if link_element is None:
                                    continue

                                link = link_element['href']

                                if "www." in link:
                                    link = link.replace('www.', '')

                                if "https://" in link:
                                    link = link.replace('https://', '')

                                if "http://" in link:
                                    link = link.replace('http://', '')

                                if "//" in link:
                                    link = link.replace('//', '')

                                if "/" in link:
                                    link = link.split("/")[0]

                                shop_name = link

                        if shop_name is not None:
                            if not shop_name == "":
                                if shop_name not in fetched_websites:
                                    if validators.domain(shop_name):
                                        print("Added entry:", shop_name)
                                        fetched_websites.append(shop_name)

                    except Exception as e:
                        print(f"Error fetching entry. Skipping ...\n"
                              f"{str(e)}"
                              )
                        continue

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
    # de -> trustedshops.de, uk -> trustedshops.co.uk
    country = "de"

    # False -> no valid TrustedShops certificate on website required.
    cert = False

    results = fetch_trustedshops_domains(country, cert=cert)

    if cert:
        output_name = f'trustedshops_all_categories_cert_{country}'
    else:
        output_name = f'trustedshops_all_categories_{country}'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
