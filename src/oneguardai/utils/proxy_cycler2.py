import requests
from lxml.html import fromstring
from itertools import cycle


class ProxyRotator:
    def __init__(self, http_proxies, https_proxies, rotation_interval=10):
        self.http_proxies = cycle(http_proxies)
        self.https_proxies = cycle(https_proxies)
        self.rotation_interval = rotation_interval
        self.rotation_count = 0
        self.current_proxy = None

    def get_next_proxy(self, protocol):
        if protocol == "http":
            self.current_proxy = next(self.http_proxies)
        elif protocol == "https":
            self.current_proxy = next(self.https_proxies)

        self.rotation_count += 1
        if self.rotation_count >= self.rotation_interval:
            self.rotation_count = 0
            self.rotate_proxies()

        return self.current_proxy

    def rotate_proxies(self):
        new_http_proxies, new_https_proxies = get_proxies()
        self.http_proxies = cycle(new_http_proxies)
        self.https_proxies = cycle(new_https_proxies)


def get_proxies(n_proxies: int = 10):
    """ Retrieve a maximum of `n_proxies` from the 'free-proxy-list.net'
    website. """
    url = "https://free-proxy-list.net/"
    url_ssl = "https://www.sslproxies.org/"

    n_proxies_ssl = n_proxies

    parser = fromstring(requests.get(url).text)
    parser_ssl = fromstring(requests.get(url_ssl).text)
    proxies = set()
    proxies_ssl = set()
    for prot in ["http", "https"]:
        if prot == "http":
            parser = parser
        else:
            parser = parser_ssl

        for line in parser.xpath('//tbody/tr'):
            if prot == "http":
                if n_proxies <= 0:
                    break
            else:
                if n_proxies_ssl <= 0:
                    break

            if line.xpath('.//td[7][contains(text(),"yes")]'):
                # Grabbing IP and corresponding port
                proxy = ":".join([line.xpath('.//td[1]/text()')[0],
                                  line.xpath('.//td[2]/text()')[0]]
                                 )

                if prot == "http":
                    proxies.add(proxy)
                    n_proxies -= 1
                else:
                    proxies_ssl.add(proxy)
                    n_proxies_ssl -= 1

    return proxies, proxies_ssl


# Beispiel-Nutzung:
rotator = ProxyRotator(*get_proxies())

for _ in range(20):
    # Hier kann zwischen "http" und "https" gewählt werden
    proxy = rotator.get_next_proxy("https")
    print(f"Using proxy: {proxy}")

    try:
        response = requests.get("https://www.example.com",
                                proxies={"https": proxy},
                                timeout=5
                                )

        url_verify = "https://api64.ipify.org"
        response_verify = requests.get(url_verify, proxies={

                "https":
                    proxy
                }
                                       )
        print("PROXY VERIFY: ", response_verify.text)

        # Führe hier die gewünschte Aktion mit der Antwort durch
        print(response.status_code)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
