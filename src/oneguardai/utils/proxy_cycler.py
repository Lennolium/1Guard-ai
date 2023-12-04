import itertools

import requests
from lxml.html import fromstring


def main():
    url = "https://api64.ipify.org"
    BATCH_SIZE_PROXIES = 10
    CYCLE_TIME = 3
    TIMEOUT = 3

    useless_proxies = []
    while True:
        proxy_pool = itertools.cycle(get_proxies(n_proxies=BATCH_SIZE_PROXIES))
        for proxy in range(BATCH_SIZE_PROXIES * CYCLE_TIME):
            proxy = next(proxy_pool)

            if proxy in useless_proxies:
                continue

            while True:
                try:
                    print("USE PROXY:", proxy)
                    response = requests.get(url, proxies={"https":
                                                              proxy
                                                          }, timeout=TIMEOUT
                                            )
                    print("CHECKED PROXY", response.text)
                    continue

                except:
                    print("PROXY USELESS")
                    useless_proxies.append(proxy)
                    break


def get_proxies(n_proxies: int = 10):
    """ Retrieve a maximum of `n_proxies` from the 'free-proxy-list.net'
    website. """
    # URL = 'https://free-proxy-list.net/'
    URL = "https://www.sslproxies.org"

    parser = fromstring(requests.get(URL).text)
    proxies = set()
    for line in parser.xpath('//tbody/tr'):
        if n_proxies <= 0:
            break

        if line.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding port
            proxy = ":".join([line.xpath('.//td[1]/text()')[0],
                              line.xpath('.//td[2]/text()')[0]]
                             )
            proxies.add(proxy)

            n_proxies -= 1
    return proxies


def get_ssl_proxy(n_proxies):
    url = "https://www.sslproxies.org"

    parser = fromstring(requests.get(url).text)
    proxies = []
    for line in parser.xpath('//tbody/tr'):
        if n_proxies <= 0:
            break

        if line.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding port
            proxy = ":".join([line.xpath('.//td[1]/text()')[0],
                              line.xpath('.//td[2]/text()')[0]]
                             )
            proxies.append(proxy)

            n_proxies -= 1

    return proxies


def request_url(url):
    proxies = get_ssl_proxy(5)
    proxies_offline = []

    # proxy_pool = itertools.cycle(proxies)

    # for proxy in proxies:

    while True:

        print("NO PROXIES LEFT, regenerating...")
        proxies = get_ssl_proxy(5)

        for proxy in proxies:

            print("Proxy list", proxies)

            if len(proxies) == 1:
                print("NO PROXIES LEFT, regenerating...")
                proxies = get_ssl_proxy(5)
                continue

            if proxy in proxies_offline:
                print("PROXY in offline list")
                continue

            try:
                print("TRY PROXY:", proxy)
                response = requests.get(url=url,
                                        proxies={"https": proxy},
                                        timeout=3
                                        )

                print("PROXY VERIFY:", response.text)
                print("SUCCESS PROXY:", proxy)
                raise Exception("TEST")
                # continue

            except Exception as e:

                print("PROXY OFFLINE", proxy)
                proxies_offline.append(proxy)
                proxies.remove(proxy)
                print("Proxy list nache excep", proxies)

                # break

    # while True:
    #
    #     if not proxies:
    #         print("NO PROXIES LEFT, regenerating...")
    #         proxies = get_ssl_proxy(5)
    #         proxy_pool = itertools.cycle(proxies)
    #
    #     proxy = next(proxy_pool)
    #
    #     if proxy in proxies_offline:
    #         continue
    #
    #     while proxies:
    #
    #         try:
    #             print("TRY PROXY:", proxy)
    #             response = requests.get(url=url,
    #                                     proxies={"https": proxy},
    #                                     timeout=3
    #                                     )
    #
    #             print("PROXY VERIFY:", response.text)
    #             print("SUCCESS PROXY:", proxy)
    #             raise Exception("TEST")
    #             continue
    #
    #         except Exception as e:
    #
    #             print("PROXY OFFLINE", proxy)
    #             proxies_offline.append(proxy)
    #             proxies.remove(proxy)
    #             # break


if __name__ == '__main__':
    # print(get_ssl_proxy(20))

    request_url("https://api64.ipify.org")

    # main()
