from email.mime import image
import io
import os
import webcolors

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import sys
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
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    print('Labels:')
    for label in labels:
        print(label.description)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    print('Properties:')

    # sort from greatest pixel fraction to smallest fraction
    newList = sorted(props.dominant_colors.colors, key=lambda x: x.pixel_fraction, reverse=True)

    for color in newList:
        # select the most common color
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
    
    red = (int)(newList[0].color.red)
    blue = (int)(newList[0].color.blue)
    green = (int)(newList[0].color.green)
    #named_color = rgb_to_name((red,green,blue), spec='css3')

    requested_colour = (red,green,blue)
    closest_name = get_colour_name(requested_colour)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return [closest_name, labels[0].description]

# Create your views here.
def index(request):
    if request.method == "POST":
        newjpgtxt = request.__dict__["_post"]["data"]

        encoded_data = newjpgtxt.split("base64,")[1]

        #decode base64 string data
        decoded_data=base64.b64decode((encoded_data))

        #write the decoded data back to original format in  file
        img_file = open('image.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()

        # url = "https://api.removal.ai/3.0/remove"

        # payload={'image_url': 'url_to_image'}
        # files=[
        # ('image_file',('image.jpeg',open('image.jpeg','rb'),'image/jpeg'))
        # ]

        # headers = {
        # 'Rm-Token': '633935662e4740.89639290'
        # }

        # response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # print(response.text)

        # image_url = response.json()["url"]

        # img_data = requests.get(image_url).content
        # with open('image_name.jpg','wb') as handler:
        #     handler.write(img_data)

        # detect_labels_uri("image_name.jpg")
        color, thing = detect_labels_uri("image.jpeg")

    return render(request, "index.html")