import requests
from bs4 import BeautifulSoup as bs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get(
    "https://www.ebay.com/sch/i.html?_nkw=Minecraft+ps3", headers=headers
).text

soup = bs(html, "lxml")

data = []

for item in soup.select(".s-item__wrapper.clearfix"):
    title = item.select_one(".s-item__title").text
    link = item.select_one(".s-item__link")["href"]
    print(title)
