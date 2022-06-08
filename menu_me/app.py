import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import base64
from io import BytesIO
import string


###############################
###### Google Vision API ######
###############################
def detect_text():
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image=vision.Image()
    image.source.image_uri='https://storage.googleapis.com/menu_me_bucket/img.jpg'

    response = client.text_detection(image=image)
    texts = response.text_annotations[0]

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return '\n"{}"'.format(texts.description)



###############################
###### Text preprocessor ######
###############################
chars_to_remove = '0123456789!"\'#$%&()*+,-./:;<=>?@[\]^_`{|}~♦●★‒…£¡™¢∞§¶•ªº–≠≠œ∑´®†¥¨≤≥÷ç√€'

words_to_remove = ['serve','served','serving','appetizer','appetizers','course','price']

drop_words = ['menu','bill','tax','consumer','advisory']

def strip(text):
    menu_original = text.split('\n')

    menu_chars_removed = []
    for item in menu_original:
        for char in chars_to_remove:
            item = item.replace(char,'')
        menu_chars_removed.append(item)

    menu_words_removed = []
    for item in menu_chars_removed:
        temporary = []
        for word in item.split(' '):
            if word.lower() not in words_to_remove:
                temporary.append(word)
        words_removed = ' '.join(temporary)
        menu_words_removed.append(words_removed)

    menu_entries_dropped = []
    for item in menu_words_removed:
        temporary = []
        for word in item.split(' '):
            if word.lower() in drop_words:
                temporary = []
                pass
            else:
                temporary.append(word)
        entries_dropped = ' '.join(temporary)
        menu_entries_dropped.append(entries_dropped)

    menu_entries_dropped = [item for item in menu_entries_dropped if len(item)>4]
    return menu_entries_dropped


##################################
######   Image Search API   ######
##################################
from google_images_search import GoogleImagesSearch
import os
from dotenv import load_dotenv, find_dotenv


#Connecting with GCP
env_path = find_dotenv()
load_dotenv(env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')

def search_image(text):
    gis = GoogleImagesSearch(GOOGLE_API_KEY, GOOGLE_CX)

    _search_params = {
        'q': f'{text} recipe',
        'num': 1
    }

    gis.search(search_params=_search_params)
    # print(gis.results())
    img_url = ''
    for image in gis.results():
        img_url = image.url  # image direct url

    return img_url



###############################
######   Translate API   ######
###############################
target='en'
def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]
