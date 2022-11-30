import requests
import random
from bs4 import BeautifulSoup as bs

def get_free_proxies():
    url = "https://free-proxy-list.net/"

    try:
        req = requests.get(url)
    finally:
        content = req.content
    soup = bs(content, "html.parser")
    proxies = []
    for row in soup.find("div", attrs={"class": "fpl-list"}).find_all("tr"):
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(("socks5", str(ip), int(port)))
        except IndexError:
            continue
    return random.choice(proxies)
