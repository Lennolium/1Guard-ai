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


def fetch_klarna_domains():
    fetched_websites = []
    count_before = 0
    count_after = 0

    stop_counter = 0

    page_url = "https://www.klarna.com/de/klarna-shops/"

    while True:

        print("---" * 20)
        print(f"NEW WHILE LOOP")

        count_before = count_after

        # response = requests.get(page_url, timeout=5)

        # Read txt file and load html.
        with open("klarna_uk_html.txt", "r") as file:
            response = file.read()

            # if response.status_code == 200:
        if True:
            # soup = BeautifulSoup(response.text, 'html.parser')
            soup = BeautifulSoup(response, 'html.parser')

            site_items = soup.find_all('div',
                                       class_='jsx-2422656473 tracking--div'
                                       )

            if not site_items:
                print("No entries found.")
                break

            for site_item in site_items:
                link = site_item.find('a')["href"]

                try:
                    link2 = link.split(
                            'https://r.klarna.com/?to=https%3A%2F%2Fwww.'
                            )[1].split('%')[0]

                except Exception:
                    try:
                        link2 = link.split(
                                'https://r.klarna.com/?to=https%3A%2F%2F'
                                )[1].split('%')[0]

                    except Exception:
                        continue

                try:
                    if "www" in link2:
                        www = link2.split(".")[0]
                        link2 = link2.replace(f"{www}.", "")

                except Exception:
                    continue

                try:
                    if "&" in link2:
                        link2 = link2.split("&")[0]

                except Exception:
                    continue

                fetched_websites.append(link2)
                print("Added entry:", link2)

            # Remove duplicates.
            fetched_websites = list(set(fetched_websites))

            count_after = len(fetched_websites)

            print(f"Count: {len(fetched_websites)}")

            continue

            if stop_counter >= 5:
                print("No new entries found. Stopping now completely!")
                print("---" * 20)
                print("Fetched domains:", len(fetched_websites))
                return fetched_websites

            if count_before == count_after:
                print("No new entries found. Waiting now for 120 seconds.")

                time.sleep(30)

                print("90 seconds left.")

                time.sleep(30)

                print("60 seconds left.")

                time.sleep(30)

                print("30 seconds left.")

                time.sleep(30)

                stop_counter += 1

                print("Continuing now.")

            else:
                stop_counter = 0

            continue

        #     html = response.text
        #
        #     print("Fetched page:", html)
        #
        #     for line in html.splitlines():
        #
        #         if 'href="https://r.klarna.com/?to=' in line:
        #             try:
        #                 link = \
        #                     line.split(
        #                             'href="https://r.klarna.com/?to=https%3A%2F%2Fwww.'
        #                             )[
        #                         1].split(
        #                             '%'
        #                             )[0]
        #
        #                 print("Link:", link)
        #
        #
        #             except Exception:
        #                 continue
        #
        #             # Check if shop name is a valid domain format.
        #             if validators.domain(link):
        #                 if "www." in link:
        #                     link = link.replace("www.", "")
        #
        #                 if "https://" in link:
        #                     link = link.replace("https://", "")
        #
        #                 if "http://" in link:
        #                     link = link.replace("http://", "")
        #
        #             else:
        #                 if "www." in link:
        #                     link = link.replace('www.', '')
        #
        #                 if "https://" in link:
        #                     link = link.replace('https://', '')
        #
        #                 if "http://" in link:
        #                     link = link.replace('http://', '')
        #
        #                 if "/" in link:
        #                     link = link.split("/")[0]
        #
        #                 if "www" in link:
        #                     www = link.split(".")[0]
        #                     link = link.replace(f"{www}.", "")
        #
        #                 if "?" in link:
        #                     link = link.split("?")[0]
        #
        #                 if link.startswith("affiliate"):
        #                     aff_split = link.split(".")[0]
        #                     link = link.replace(f"{aff_split}.", "")
        #
        #             if link is not None:
        #                 if not link == "":
        #                     if link not in fetched_websites:
        #                         if validators.domain(link):
        #                             print("Added entry:", link)
        #                             fetched_websites.append(link)
        #
        #
        #
        # else:
        #     print("All entries fetched.")
        #     break


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
    # response = requests.get(url, timeout=5)

    # soup = BeautifulSoup(response.text, 'html.parser')

    # link = site_items.find_all('a')['href']

    # print(link)

    # print(site_items)

    # print(soup.prettify())

    results = fetch_klarna_domains()

    output_name = f'klarna_all_categories'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
