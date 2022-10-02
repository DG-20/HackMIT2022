import io
import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import sys
from django.http import HttpResponse
import base64

# Imports the Google Cloud client library
from google.cloud import vision

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
    newlist = sorted(props.dominant_colors.colors, key=lambda x: x.pixel_fraction, reverse=True)

    for color in newlist:
        # select the most common color
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

# Create your views here.
def index(request):
    if request.method == "POST":
        #png_recovered = base64.decodestring((request.__dict__["_post"]["data"]))
        newjpgtxt = request.__dict__["_post"]["data"]

        encoded_data = newjpgtxt.split("base64,")[1]

        #decode base64 string data
        decoded_data=base64.b64decode((encoded_data))

        #write the decoded data back to original format in  file
        img_file = open('image.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()

        detect_labels_uri("image.jpeg")

    return render(request, "index.html")