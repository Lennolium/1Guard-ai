#!/usr/bin/env python3

"""
fetch_data.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-24"
__status__ = "Prototype/Development/Production"

# Imports.
import logging
import csv
import time

from oneguardai import const
from oneguardai.data import features
from oneguardai.utils import log

# Root logger and log counter.
if __name__ == "__main__":
    # Root logger and log counter.
    LOG_COUNT = log.LogCount()
    LOGGER = log.create(LOG_COUNT)
else:
    # Child logger.
    LOGGER = logging.getLogger(__name__)


def process_domains(input_file_path: str, output_file_path: str, trust: bool) \
        -> None:
    domains_offline = []

    # Read domains from file line by line and open the csv output file.
    with open(input_file_path, "r") as input_file, \
            open(output_file_path,
                 mode="w",
                 newline="",
                 encoding="utf-8"
                 ) as csv_file:

        domains = input_file.read().splitlines()

        domains_count = len(domains)

        writer = csv.writer(csv_file, delimiter=",")

        # Write header aka column names.
        header = ["DOMAIN"] + features.WebsiteFeatures.features_names + [
                "TRUST"]
        writer.writerow(header)

        start_time = time.perf_counter()

        progress = 0

        for domain in domains:

            # Print and log progress.
            progress += 1
            LOGGER.info(f"Progress: {progress}/{domains_count} domains.")

            features_obj = features.WebsiteFeatures(domain)

            # Check if website is reachable and fetchable.
            if (features_obj.alive is False) or (
                    features_obj.fetchable is False):
                domains_offline.append(domain)
                LOGGER.info(f"Skipping: {domain}")
                LOGGER.info("--------------------------------------------")
                continue

            # Start the website and feature extraction.
            features_obj.feature_extraction()

            # Construct the row for the csv file.
            # Trust column: 1 = trusted, 0 = not trusted/scam.
            row = [domain] + features_obj.features + [trust * 1]

            writer.writerow(row)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        LOGGER.info(f"Finished processing all {domains_count} domains in "
                    f"{elapsed_time:.2f} s."
                    )
        LOGGER.info("Mean time per domain: "
                    f"{elapsed_time / domains_count:.2f} s/domain."
                    )
        LOGGER.info("------------------- END: -------------------")

        # Write offline domains to separate file.
        output_offline_file = f"{input_file_path[:-4]}_offline.txt"
        with open(output_offline_file, 'w') as offline_file:
            for domain_offline in domains_offline:
                offline_file.write(domain_offline + '\n')


if __name__ == "__main__":
    input_file_path = f"{const.APP_PATH}/data/sources/domains.txt"
    output_file_path = f"{const.APP_PATH}/data/output.csv"

    process_domains(input_file_path, output_file_path, trust=False)
