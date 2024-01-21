from googlesearch import search

import yagooglesearch


def google_search():
    query = "discount clothing store site:*.com"

    client = yagooglesearch.SearchClient(
            query,
            # tbs="li:1",
            max_search_result_urls_to_return=1000,
            http_429_cool_off_time_in_minutes=1,
            http_429_cool_off_factor=1.5,
            # proxy="socks5h://127.0.0.1:9050",
            verbosity=5,
            verbose_output=False
            )
    client.assign_random_user_agent()

    urls = client.search()

    len(urls)

    for url in urls:
        print(url)


def search_and_extract_domains(search_query, num_results, output_file, lang,
                               tld=None
                               ):
    try:
        with open(output_file, 'w') as file:

            if tld is None:
                query = f"{search_query}"
            else:
                query = f"{search_query} site:*{tld}"

            results = search(query, num_results=num_results, lang=lang,
                             sleep_interval=2
                             )

            results_set = []

            # Extrahiere und schreibe die Domains in die Datei
            for result in results:
                domain = result.split("//")[-1].split("/")[0].split('?')[0]

                if domain.startswith("www."):
                    domain = domain[4:]

                if domain.startswith("www2."):
                    domain = domain[4:]

                if domain.startswith("www3."):
                    domain = domain[4:]

                if domain.startswith("."):
                    domain = domain[1:]

                no_sub = domain.split(".", maxsplit=1)[-1]
                if no_sub in results_set:
                    print("Skipped:", domain)
                    continue

                if domain not in results_set:
                    results_set.append(domain)

                    file.write(domain + '\n')

                    print("Added:", domain)

                else:
                    print("Skipped:", domain)

            print(f"Es wurden {len(results_set)} Domains gefunden.")


    except Exception as e:
        print(f"Fehler: {e}")


# Beispielaufruf

google_search()

exit()
language = "en"
tld = ".com"
search_query = "discount clothing store"
num_results = 1000
output_file = "google_fetched.txt"
search_and_extract_domains(search_query, num_results, output_file,
                           language, tld
                           )
