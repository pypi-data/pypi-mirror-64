# https://fopina.github.io/tgbot-pushitbot/#api-docs
import requests
from bs4 import BeautifulSoup
import json

def get_token(address):
    def get_raw_link(address):
        soup = BeautifulSoup(requests.get(address).text, 'lxml')
        for link in soup.find_all('a'):
            link = str(link.get('href'))
            link = link if "/raw/" in link else None
            if link:
                if link.startswith("/"):
                    return "https://gist.githubusercontent.com"+link

    if not address.startswith("https://gist.githubusercontent.com/"):
        address = get_raw_link(address)
    return json.loads(requests.get(address).text)['pushitbot']

def send_message(string, token):
    string = string.replace(" ", '+')
    r = requests.get("https://tgbots.skmobi.com/pushit/{}?msg={}".format(token,string))
    return r
