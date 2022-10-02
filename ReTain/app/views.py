from email.mime import image
import io
import os
import webcolors

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
import base64
import requests
from webcolors import rgb_to_name
from bs4 import BeautifulSoup as bs

# Imports the Google Cloud client library
from google.cloud import vision

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return closest_name

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

    # sort from greatest pixel fraction to smallest fraction to select the most common color
    newList = sorted(
        props.dominant_colors.colors, key=lambda x: x.pixel_fraction, reverse=True
    )
    
    red = (int)(newList[0].color.red)
    blue = (int)(newList[0].color.blue)
    green = (int)(newList[0].color.green)

    requested_colour = (red,green,blue)
    closest_name = get_colour_name(requested_colour)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return [closest_name, labels[0].description]

# Create your views here.
def index(request):
    if request.method == "POST":
        newjpgtxt = request.__dict__["_post"]["data"]

        encoded_data = newjpgtxt.split("base64,")[1]

        # decode base64 string data
        decoded_data = base64.b64decode((encoded_data))

        # write the decoded data back to original format in  file
        img_file = open("image.jpeg", "wb")
        img_file.write(decoded_data)
        img_file.close()

        url = "https://api.removal.ai/3.0/remove"

        payload={'image_url': 'url_to_image'}
        files=[
        ('image_file',('image.jpeg',open('image.jpeg','rb'),'image/jpeg'))
        ]

        headers = {
        'Rm-Token': '633973f617eed6.50836218'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        image_url = response.json()["url"]

        img_data = requests.get(image_url).content
        with open('image_name.jpg','wb') as handler:
            handler.write(img_data)

        color, thing = detect_labels_uri("image_name.jpg")

        print("Results: "+color+" "+thing)

        headers_ebay = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

        html_ebay = requests.get(
            f"https://www.ebay.com/sch/i.html?_nkw={color}+{thing}", headers=headers_ebay
        ).text

        soup_ebay = bs(html_ebay, "lxml")

        ebay_items = []

        for item in soup_ebay.select(".s-item__wrapper.clearfix"):
            try:
                if(item.select(".SECONDARY_INFO") is not None):
                    if item.select(".SECONDARY_INFO")[0].text == "Pre-Owned":
                        title = item.select_one(".s-item__title").text
                        link = item.select_one(".s-item__link")["href"]
                        price = item.select_one(".s-item__price").text
                        img = item.select_one(".s-item__image-img")["src"]
                        ebay_items.append(
                            {"title": title, "link": link, "price": price, "img": img}
                        )
            except:
                continue

        html_kijiji = requests.get(
            f"https://www.kijiji.ca/b-city-of-toronto/{color}-{thing}/k0l1700273?rb=true&ll=43.653226%2C-79.383184&address=Toronto%2C+ON&radius=50.0&dc=true",
            headers=headers_ebay,
        ).text

        soup_kijiji = bs(html_kijiji, "lxml")

        kijiji_items = []



        for item in soup_kijiji.select(".s-item__wrapper.clearfix"):
            try:
                if item.select(".SECONDARY_INFO")[0].text == "Pre-Owned":
                    title = item.select_one(".s-item__title").text
                    link = item.select_one(".s-item__link")["href"]
                    price = item.select_one(".s-item__price").text
                    img = item.select_one(".s-item__image-img")["src"]
                    kijiji_items.append(
                        {"title": title, "link": link, "price": price, "img": img}
                    )
            except:
                continue

        kijiji_str = ""
        for item in kijiji_items:
            kijiji_str += item["title"]
            kijiji_str += "\n"
            kijiji_str += item["link"]
            kijiji_str += "\n"
            kijiji_str += item["price"]
            kijiji_str += ""
            kijiji_str += item["img"]
            kijiji_str += "\n\n"

        ebay_str = ""
        for item in ebay_items:
            ebay_str += item["title"]
            ebay_str += "\n"
            ebaystr += item["link"]
            ebay_str += "\n"
            ebay_str += item["price"]
            ebay_str += ""
            ebay_str += item["img"]
            ebay_str += "\n\n"

        with open("kijiji.txt", "w") as f_out:
            f_out.write(kijiji_str)

        with open("ebay.txt", "w") as f_out:
            f_out.write(ebay_str)
            
        return render(request, "index.html")

    else:  
        return render(request, "index.html")