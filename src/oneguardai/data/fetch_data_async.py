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
import asyncio
import csv
import logging
import time
from concurrent.futures import CancelledError
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


class ProgressState:
    def __init__(self):
        self.progress = 0
        self.domains_offline = []
        self.domain = None
        self.domains_count = None


progress_state = ProgressState()


async def process_domain_async(domain, progress_state):
    LOGGER.info(
            f"Progress: {progress_state.progress}/"
            f"{progress_state.domains_count} "
            f"domains. Processing: {domain}"
            )
    features_obj = features.WebsiteFeatures(domain)

    # Check if website is reachable and fetchable.
    if (features_obj.alive is False) or (features_obj.fetchable is False):
        LOGGER.info(f"Skipping: {domain}")
        LOGGER.info("--------------------------------------------")
        return None

    # Start the website and feature extraction.
    features_obj.feature_extraction()

    # Trust column: 1 = trusted, 0 = not trusted/scam.
    return [domain] + features_obj.features + [trust * 1]


async def update_progress_async(result, writer, lock, progress_state):
    if result is not None:
        async with lock:
            writer.writerow(result)
    else:
        progress_state.domains_offline.append(progress_state.domain)

    progress_state.progress += 1
    LOGGER.info(
            f"Progress: {progress_state.progress}/"
            f"{progress_state.domains_count} "
            f"domains."
            )


async def process_domains_async(input_file_path: str, output_file_path: str,
                                trust: bool, max_concurrent: int = 5
                                ):
    progress_state.progress = 0
    progress_state.domains_offline = []
    progress_state.domain = None
    progress_state.domains_count = None

    # Read domains from file line by line.
    with open(input_file_path, "r") as input_file:
        domains = input_file.read().splitlines()

    progress_state.domains_count = len(domains)

    # Write header aka column names.
    header = ["DOMAIN"] + features.WebsiteFeatures.features_names + ["TRUST"]

    with open(output_file_path, mode="w", newline="", encoding="utf-8"
              ) as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(header)
        lock = asyncio.Lock()

        start_time = time.perf_counter()

        async def process_domains_inner():
            tasks = []
            for progress_state.domain in domains:
                task = asyncio.create_task(
                        process_domain_async(progress_state.domain,
                                             progress_state
                                             )
                        )
                task.add_done_callback(
                        lambda t: update_progress_async(t.result(), writer,
                                                        lock,
                                                        progress_state
                                                        )
                        )
                tasks.append(task)

            try:
                await asyncio.gather(*tasks)
            except CancelledError:
                pass

        await asyncio.run(process_domains_inner())

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        LOGGER.info(
                f"Finished processing all {progress_state.domains_count} "
                f"domains "
                f"in "
                f"{elapsed_time:.2f} s."
                )
        LOGGER.info("Mean time per domain: "
                    f"{elapsed_time / progress_state.domains_count:.2f} "
                    f"s/domain."
                    )
        LOGGER.info("------------------- END: -------------------")

        # Write offline domains to separate file.
        output_offline_file = f"{input_file_path[:-4]}_offline.txt"
        with open(output_offline_file, 'w') as offline_file:
            for domain_offline in progress_state.domains_offline:
                offline_file.write(domain_offline + '\n')


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(process_domains_async(
                f"{const.APP_PATH}/data/sources/domains.txt",
                f"{const.APP_PATH}/data/output.csv",
                trust=False
                )
                )
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
