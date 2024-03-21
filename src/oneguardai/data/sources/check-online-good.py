#!/usr/bin/env python3

"""
check-online-bad.py: TODO: Headline...

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
import os
from datetime import timedelta
import concurrent.futures
import requests
import time


def check_domain(domain):
    url_ssl = f"https://{domain}"
    url = f"http://{domain}"
    drop = False

    try:
        response = requests.head(url_ssl, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            status = "SSL"
        else:
            raise requests.ConnectionError
    except Exception:
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                status = "NO SSL"
            else:
                raise requests.ConnectionError
        except Exception:
            status = "DROPPED"
            drop = True

    ssl_status = " ✓" if status == "SSL" else " ✗"
    no_ssl_status = " ✓" if status == "NO SSL" else " ✗"
    if drop:
        print(f"{ssl_status}        {no_ssl_status}        {domain} "
              f"➞ DROPPED"
              )
    else:
        print(f"{ssl_status}        {no_ssl_status}        {domain}")

    return domain, status


def check_online_domains(input_file,
                         output_file,
                         output_file_offline,
                         parallel=True,
                         progress_interval=100,
                         max_workers=None
                         ):
    # Default value of max_workers from ThreadPoolExecutor.
    if not max_workers:
        max_workers = min(32, (os.cpu_count() or 1) + 4)
        print(f"Using {max_workers} max_workers.")

    with open(input_file, 'r') as f:
        domains = [line.strip() for line in f.readlines()]

    online_domains = []
    offline_domains = []

    domains_total = len(domains)
    print(f"Checking {domains_total} domains for online status.")
    domain_count = 0

    time_start = time.perf_counter()

    with (concurrent.futures.ThreadPoolExecutor(max_workers=max_workers
                                                ) if parallel
          else
          concurrent.futures.ProcessPoolExecutor() as executor):
        futures = {executor.submit(check_domain, domain): domain for domain in
                   domains}
        for future in concurrent.futures.as_completed(futures):
            domain, status = future.result()
            domain_count += 1

            if domain_count % progress_interval == 0 or (domain_count ==
                                                         domains_total):
                time_end = time.perf_counter()
                time_elapsed = time_end - time_start
                time_elapsed_readable = str(timedelta(seconds=time_elapsed))

                try:
                    time_remaining = (time_elapsed / domain_count) * (
                            domains_total - domain_count)
                    time_remaining_readable = str(
                            timedelta(seconds=time_remaining)
                            )
                except ZeroDivisionError:
                    time_remaining_readable = "0:00:00:00"

                print("---" * 10)
                print(f"Checked {domain_count}/{domains_total} domains.")
                print(f"Time elapsed: {time_elapsed_readable} dd:hh:mm:ss.")
                print(
                        f"Time remaining: {time_remaining_readable} "
                        f"dd:hh:mm:ss."
                        )
                print("---" * 10)
                print("SSL     NO SSL     DOMAIN")

            if status == "DROPPED":
                offline_domains.append(domain)
            else:
                online_domains.append(domain)

    time_end = time.perf_counter()
    time_elapsed = time_end - time_start
    time_elapsed_readable = str(timedelta(seconds=time_elapsed))

    print("---" * 10)
    print("----- RESULTS: -----")
    print(f"Checked domains: {domains_total}.")
    print(f"Online domains: {len(online_domains)}.")
    print(f"Time elapsed: {time_elapsed_readable} dd:hh:mm:ss.")
    print("---" * 10)

    with open(output_file, 'w') as f:
        for online_domain in online_domains:
            f.write(f"{online_domain}\n")

    with open(output_file_offline, 'w') as f2:
        for offline_domain in offline_domains:
            f2.write(f"{offline_domain}\n")


if __name__ == "__main__":
    input_file_path = "combined_good/combined_good.txt"
    output_file_path = "online_domains/output_good_online.txt"
    output_offline_fp = "offline_domains/output_good_offline.txt"

    check_online_domains(input_file_path, output_file_path, output_offline_fp,
                         parallel=True, progress_interval=100, max_workers=32
                         )

# def check_online_domains(input_file, output_file, output_file_offline):
#     with open(input_file, 'r') as f:
#         domains = [line.strip() for line in f.readlines()]
#
#     online_domains = []
#     offline_domains = []
#
#     domains_total = len(domains)
#     print(f"Checking {domains_total} domains for online status.")
#     domain_count = 0
#
#     time_start = time.perf_counter()
#
#     for domain in domains:
#
#         if domain_count % 100 == 0:
#
#             time_end = time.perf_counter()
#             time_elapsed = time_end - time_start
#             time_elapsed_readable = str(timedelta(seconds=time_elapsed))
#             if "." in time_elapsed_readable:
#                 time_elapsed_readable = \
#                     time_elapsed_readable.split(".")[0]
#
#             # Remaining time.
#             try:
#                 time_remaining = (time_elapsed / domain_count) * (
#                         domains_total - domain_count)
#                 time_remaining_readable = str(
#                         timedelta(seconds=time_remaining)
#                         )
#                 if "." in time_remaining_readable:
#                     time_remaining_readable = \
#                         time_remaining_readable.split(".")[0]
#
#             except ZeroDivisionError:
#                 time_remaining_readable = "0:00:00:00"
#
#             print("---" * 10)
#             print(f"Checked {domain_count}/{domains_total} domains.")
#             print(f"Time elapsed: {time_elapsed_readable} dd:hh:mm:ss.")
#             print(f"Time remaining: {time_remaining_readable} dd:hh:mm:ss.")
#             print("---" * 10)
#             print("SSL     NO SSL     DOMAIN")
#
#         domain_count += 1
#
#         # Skip empty lines.
#         if domain == "":
#             continue
#
#         # Skip comments.
#         if domain.startswith("#"):
#             continue
#
#         # Remove http:// and https:// from the domain.
#         if domain.startswith("http://") or domain.startswith("https://"):
#             domain = domain.replace("http://", "")
#             domain = domain.replace("https://", "")
#
#         url = f"http://{domain}"
#         url_ssl = f"https://{domain}"
#
#         # Try to connect to the domain with SSL first.
#         try:
#             print(f"                   {domain}\r", end="", sep="")
#             response = requests.head(url_ssl, timeout=5,
#                                      allow_redirects=True
#                                      )
#             if response.status_code == 200:
#                 online_domains.append(domain)
#                 print(f" ✓        -        {domain}")
#             else:
#
#                 raise requests.ConnectionError
#
#         # If SSL connection fails, try to connect without SSL.
#         except Exception:
#             print(f" ✗                 {domain}\r", end="", sep="")
#             try:
#                 response = requests.head(url, timeout=5,
#                 allow_redirects=True)
#                 if response.status_code == 200:
#                     online_domains.append(domain)
#                     print(f" ✗        ✓        {domain}")
#                 else:
#
#                     raise requests.ConnectionError
#
#             except Exception:
#                 print(f" ✗        ✗        {domain} ➞ DROPPED")
#                 offline_domains.append(domain)
#
#     # Elapsed time.
#     time_end = time.perf_counter()
#     time_elapsed = time_end - time_start
#     time_elapsed_readable = str(timedelta(seconds=time_elapsed))
#
#     # Print results.
#     print("---" * 10)
#     print("----- RESULTS: -----")
#     print(f"Checked domains: {domains_total}.")
#     print(f"Online domains: {len(online_domains)}.")
#     print(f"Time elapsed: {time_elapsed_readable} dd:hh:mm:ss.")
#     print("---" * 10)
#
#     with open(output_file, 'w') as f:
#         for online_domain in online_domains:
#             f.write(f"{online_domain}\n")
#
#     with open(output_file_offline, 'w') as f2:
#         for offline_domain in offline_domains:
#             f2.write(f"{offline_domain}\n")
#
#
# if __name__ == "__main__":
#     input_file_path = "output/output_good.txt"
#     output_file_path = "output/output_good_online.txt"
#     output_offline_fp = "output/output_good_offline.txt"
#
#     check_online_domains(input_file_path, output_file_path,
#     output_offline_fp)
