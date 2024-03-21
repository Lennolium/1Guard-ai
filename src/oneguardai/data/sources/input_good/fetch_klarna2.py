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

import re


def extract_url(input_file):
    # Öffne die Datei im Lesemodus
    with open(input_file, 'r') as file:
        pattern = (r"https://r\.klarna\.com/\?to=https%3A%2F%2([A-Za-z]+(\.["
                   r"A-Za-z]+)+)%2Fde%2F\\u0026channel=klarna\.com"
                   r"\\u0026source=shops")

        pattern2 = (
                r"https://r\.klar\.na/\?to=https://([A-Za-z0-9]+(\.["
                r"A-Za-z0-9]+)+)/de/\?utm_source=klarna\\u0026utm_medium=web"
                r"\?")

        # Lese den Inhalt der Datei
        content = file.read()

        # Suche nach Übereinstimmungen im Text
        matches = re.findall(pattern, content)

        matches2 = re.findall(pattern2, content)

        print(matches2)

        matches_final = []

        for match in matches:
            if match[0].startswith('www.'):
                matchi = match[0]
                matches_final.append(matchi[4:])

            elif match[0].startswith('Fwww.'):
                matchi = match[0]
                matches_final.append(matchi[5:])

            elif match[0].startswith('F'):
                matchi = match[0]
                matches_final.append(matchi[1:])

            else:
                matches_final.append(match[0])

        for match2 in matches2:
            if match2[0].startswith('www.'):
                match3 = match2[0]
                matches_final.append(match3[4:])

            else:
                matches_final.append(match2[0])

        # Entferne Duplikate, indem die Liste in ein Set umgewandelt und
        # dann wieder in eine Liste zurückgewandelt wird
        unique_matches = list(set(matches_final))

        print(f"Found {len(unique_matches)} unique matches.")

        return unique_matches


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

    results = extract_url('klarna_uk_html.txt')

    output_name = f'klarna_all_categories_uk2'

    write_to_txt(results, output_name)

    length_domains = length(output_name)
    print(f"The file {output_name}.txt has {length_domains} domains in total.")
