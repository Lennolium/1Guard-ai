#!/usr/bin/env python3

"""
get_headers.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2024-01-24"
__status__ = "Prototype/Development/Production"

# Imports.
import http.server
import socketserver
from multiprocessing import Process


def header_referer():
    port = 8000

    # Windows vm: 10.211.55.2, local: 127.0.0.1, ds: 192.168.178.16
    # iPhone WiFi sharing: 172.20.10.11

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
        <html>
        <body>
        <button onclick="window.location.href='http://127.0.0.1:8001'">
        Click me
        </button>
        </body>
        </html>
        '''
                             )

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"REFERER: http://127.0.0.1:{port}")
        httpd.serve_forever()


def header_order():
    import socket
    # windows vm: 10.211.55.2, local: 127.0.0.1, ds: 192.168.178.16
    # iPhone WiFi sharing: 172.20.10.11
    host = "127.0.0.1"
    port = 8001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"ORDER: http://{host}:{port}")
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)

                if not data.decode().startswith("GET /favicon.ico"):
                    print(data.decode())
                # header
                conn.send(b'HTTP/1.1 200 OK\n')
                conn.send(b'Content-Type: text/html\n')
                conn.send(b'\n')
                # body
                conn.send(b'<html><body><pre>')
                conn.send(data)
                conn.send(b'</pre></body></html>')
                conn.close()


# from flask import Flask, request
#
# app = Flask(__name__)
#
#
# # Mobile: vpn ds mit ag, ip: 172.22.137.232:5000 -> script in shell laufen
# # nicht in pycharm!
# @app.route("/", methods=["GET", "POST"])
# def index():
#     # Remove Content-Length and Type header.
#     headers_conv = dict(request.headers)
#     headers_conv.pop("Content-Length", None)
#     headers_conv.pop("Content-Type", None)
#     headers_conv.pop("Origin", None)
#
#     for key, value in headers_conv.items():
#         print(f"{key}:", value)
#
#     return "<br>".join(
#             list(map(lambda i: f"{i[0]}: {i[1]}", headers_conv.items()))
#             ) + """
#     <p><form method="POST"><input type="submit" name="submit"
#     value="Submit"></form></p>"""


def tablet():
    import requests
    from bs4 import BeautifulSoup

    ua = []

    endpoint = {
            "apple": "https://useragents.io/explore/devices/types/tablet"
                     "/maker/apple-inc-b93",
            "google": "https://useragents.io/explore/devices/types/tablet"
                      "/maker/google-inc-f3d"
            }

    for device, endpoint in endpoint.items():
        print(device, endpoint)

        response = requests.get(url=endpoint,
                                timeout=5,
                                allow_redirects=True
                                )

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select('td > a')

        # user_agents = [a.get_text(strip=True) for a in soup.select('td > a')]

        for row in rows:
            content = row.get_text(strip=True)

            # Small fix for website also displaying Apple devices.
            if device == "google":
                if ("iPad" in content
                        or "iPhone" in content
                        or "iPod" in content
                        or "Mac OS X" in content):
                    continue

            ua.append(content)

        print(device, len(ua))

    # TODO: !!!! Also ab hier immer abwechselnd apple und google UAs
    #  nehmen absteigend nach Popularität sortiert. so ist es
    #  repräsentativer. !!!!

    print("FINAL:", len(ua))
    print(ua)

    # Remove newlines and whitespaces.
    # content = content.replace("\n", "").replace("  ", "")


if __name__ == "__main__":
    lol = [1, 2, 3, 4]

    print("XD:", lol[1:])

    exit(0)

    # best header order finder:
    # app.run(host='0.0.0.0', port=5000, debug=True)

    exit()
    # res = tablet()
    # print(res)

    # exit()
    p1 = Process(target=header_order)
    p2 = Process(target=header_referer)

    # Start both processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()
