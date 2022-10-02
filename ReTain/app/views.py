import io
import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import sys
from django.http import HttpResponse
import base64
# Imports the Google Cloud client library
from google.cloud import vision

# Create your views here.
def index(request):
    if request.method == "POST":
        png_recovered = base64.decodestring((request.__dict__["_post"]["data"]))

    return render(request, "index.html")

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

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_labels_uri("resources/various-shirts-men-clothes-store-shopping-mall-sale-88135317.jpg")