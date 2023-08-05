import requests
from bs4 import BeautifulSoup

__author__ = "Engine Bai"
url = "http://trust-api-trust-staging.192.168.99.100.nip.io/api/v5/api-docs/#/"

req = requests.get(url)
#html = BeautifulSoup(req.text, "html.parser")
#content_tag = html.find("div", attrs={"class": "topbar",
#                                      "data-source": "post_page"})
print(req.text)