import io
import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
import base64
import requests
from bs4 import BeautifulSoup as bs

# Imports the Google Cloud client library
from google.cloud import vision


def detect_labels_uri(path_name):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath(path_name)

    # Loads the image into memory
    with io.open(file_name, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    # sort from greatest pixel fraction to smallest fraction
    newlist = sorted(
        props.dominant_colors.colors, key=lambda x: x.pixel_fraction, reverse=True
    )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


# Create your views here.
def index(request):
    if request.method == "POST":
        # png_recovered = base64.decodestring((request.__dict__["_post"]["data"]))
        newjpgtxt = request.__dict__["_post"]["data"]

        encoded_data = newjpgtxt.split("base64,")[1]

        # decode base64 string data
        decoded_data = base64.b64decode((encoded_data))

        # write the decoded data back to original format in  file
        img_file = open("image.jpeg", "wb")
        img_file.write(decoded_data)
        img_file.close()

        detect_labels_uri("image.jpeg")

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
                ebay_items.append(
                    {"title": title, "link": link, "price": price, "img": img}
                )

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
                kijiji_items.append(
                    {"title": title, "link": link, "price": price, "img": img}
                )

        return render(
            request, "index.html", {"ebay": ebay_items, "kijiji": kijiji_items}
        )

    return render(request, "index.html")
