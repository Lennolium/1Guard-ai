#!/usr/bin/env python3

"""
feature_extraction.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-24"
__status__ = "Prototype"

# Imports.
import logging
import csv
import os
import random
import time
import datetime
import concurrent.futures

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


def load_domains(folder_path=None) -> dict[str, str]:
    if not folder_path:
        folder_path = const.DOMAINS_FOLDER

    files = sorted(os.listdir(folder_path))

    # Remove hidden files and folders (fixes errors with .DS_Store
    # on macOS).
    for file in files:
        if file.startswith("."):
            files.remove(file)

    bad_file = None
    good_file = None

    for file in files:
        # Get the newest bad domains file (sorted by name).
        if "bad" in file:
            bad_file = file

        # Get the newest good domains file.
        elif "good" in file:
            good_file = file

    if not bad_file or not good_file:
        raise FileNotFoundError(
                "Could not find bad and good domains file in "
                f"{const.DOMAINS_FOLDER}."
                )

    return {"good": f"{folder_path}/{good_file}",
            "bad": f"{folder_path}/{bad_file}"
            }


def numerate_file_name(path: str, trust: bool) -> str:
    filename, extension = os.path.splitext(path)
    counter = 1

    if trust:
        prefix = "good"
    else:
        prefix = "bad"

    path = f"{filename}_{prefix}{counter:02d}{extension}"

    while os.path.exists(path):
        counter += 1
        path = f"{filename}_{prefix}{counter:02d}{extension}"

    return path


def extract_features_for_domain(domain, trust):
    features_obj = features.WebsiteFeatures(domain)
    features_obj.feature_extraction()
    row = [domain] + features_obj.features + [trust * 1]
    return row


def extraction(csv_output_path: str = None) -> bool:
    if not csv_output_path:
        csv_output_path = const.CSV_OUTPUT

    LOGGER.info("----------- FEATURE EXTRACTION -------------")

    domain_files = load_domains()
    for key in domain_files:
        if key == "good":
            trust = 1
            continue  # Skip good domains for now.
        else:
            trust = 0

        csv_output_path = numerate_file_name(csv_output_path,
                                             trust=bool(trust)
                                             )

        with open(csv_output_path, mode="w", newline="", encoding="utf-8"
                  ) as csv_fh:
            writer = csv.writer(csv_fh, delimiter=",")
            header = ["DOMAIN"] + features.WebsiteFeatures.features_names + [
                    "TRUST"]
            writer.writerow(header)

            LOGGER.info(
                    f"Loaded csv output file '"
                    f"{csv_output_path.rsplit('/')[-1]}' "
                    f"and wrote header in it."
                    )

            input_file = domain_files[key]
            input_file_split = input_file.rsplit("/")[-1]

            with open(input_file, "r") as input_fh:
                domains = [domain.strip() for domain in input_fh.readlines()]
                random.SystemRandom().shuffle(domains)
                domains = domains[:2500]  # Limit to 2.5k domains (for now).
                domains_count = len(domains)

            LOGGER.info(
                    f"Processing {domains_count} {key} domains from '"
                    f"{input_file_split}'"
                    )

            time_start = time.perf_counter()
            progress = 0

            try:

                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as \
                        executor:
                    rows = list(
                            executor.map(extract_features_for_domain, domains,
                                         [trust] * domains_count
                                         )
                            )

                for row in rows:
                    writer.writerow(row)

                    progress += 1

                    if progress % 100 == 0:
                        time_end = time.perf_counter()
                        time_elapsed = time_end - time_start
                        time_elapsed_readable = str(
                                datetime.timedelta(seconds=time_elapsed)
                                )

                        try:
                            time_remaining = (time_elapsed / progress) * (
                                    domains_count - progress)
                            time_remaining_readable = str(
                                    datetime.timedelta(seconds=time_remaining)
                                    )
                        except ZeroDivisionError:
                            time_remaining_readable = "0:00:00:00"

                        LOGGER.info(
                                "----------------- PROGRESS -----------------"
                                )
                        LOGGER.info(
                                f"Checked {progress}/{domains_count} domains."
                                )
                        LOGGER.info(
                                f"Time elapsed: {time_elapsed_readable} "
                                f"dd:hh:mm:ss."
                                )
                        LOGGER.info(
                                f"Time remaining: {time_remaining_readable} "
                                f"dd:hh:mm:ss."
                                )
                        LOGGER.info(
                                "--------------------------------------------"
                                )


            except Exception as e:
                LOGGER.error(f"An error occurred: {e}")
                LOGGER.info(
                        "Writing collected data to CSV file before exiting..."
                        )

                for row in rows:
                    writer.writerow(row)

                LOGGER.info("Data successfully written to CSV file.")
                return False

    return True


if __name__ == "__main__":
    extraction()
