#!/usr/bin/env python3

"""
remove_offline.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-27"
__status__ = "Prototype/Development/Production"

# Imports.
import os


def remove_offline_domains():
    # Paths
    actual_folder = os.path.dirname(os.path.abspath(__file__))
    all_domains_filepath = os.path.join(actual_folder, 'domains.txt')
    offline_domains_filepath = os.path.join(actual_folder,
                                            'domains_offline.txt'
                                            )
    output_filepath = all_domains_filepath

    # Lese alle Domains aus der Datei mit allen Domains ein
    with open(all_domains_filepath, 'r') as all_domains_file:
        all_domains = set(all_domains_file.read().splitlines())

    # Lese offline Domains aus der Datei mit offline Domains ein
    with open(offline_domains_filepath, 'r') as offline_domains_file:
        offline_domains = set(offline_domains_file.read().splitlines())

    # Entferne offline Domains aus der Liste aller Domains
    remaining_domains = all_domains - offline_domains

    print(f"Remaining domains: {len(remaining_domains)}")

    # Schreibe die verbleibenden Domains in die Ausgabedatei
    with open(output_filepath, 'w') as output_file:
        output_file.write('\n'.join(remaining_domains))

    print(f"Successfully removed {len(offline_domains)} offline domains.")
    print(f"Written remaining {len(remaining_domains)} domains to domains.txt."
          )


if __name__ == '__main__':
    remove_offline_domains()
