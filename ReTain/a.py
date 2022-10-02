import requests
from bs4 import BeautifulSoup as bs

headers_ebay = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html_ebay = requests.get(
    "https://www.ebay.com/sch/i.html?_nkw=Minecraft+ps3", headers=headers_ebay
).text

soup_ebay = bs(html_ebay, "lxml")

ebay_items = []

for item in soup_ebay.select(".s-item__wrapper.clearfix"):
    if item.select(".SECONDARY_INFO")[0].text == "Pre-Owned":
        title = item.select_one(".s-item__title").text
        link = item.select_one(".s-item__link")["href"]
        price = item.select_one(".s-item__price").text
        img = item.select_one(".s-item__image-img")["src"]
        ebay_items.append({"title": title, "link": link, "price": price, "img": img})

html_kijiji = requests.get(
    f"https://www.kijiji.ca/b-city-of-toronto/pink-shirt/k0l1700273?rb=true&ll=43.653226%2C-79.383184&address=Toronto%2C+ON&radius=50.0&dc=true",
    headers=headers_ebay,
).text

soup_kijiji = bs(html_kijiji, "lxml")

kijiji_items = []

for item in soup_kijiji.select(".s-item__wrapper.clearfix"):
    if item.select(".SECONDARY_INFO")[0].text == "Pre-Owned":
        title = item.select_one(".s-item__title").text
        link = item.select_one(".s-item__link")["href"]
        price = item.select_one(".s-item__price").text
        img = item.select_one(".s-item__image-img")["src"]
        kijiji_items.append({"title": title, "link": link, "price": price, "img": img})
