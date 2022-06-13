import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from io import BytesIO
import string
#import base64
from google_images_search import GoogleImagesSearch
import os
from google.oauth2 import service_account
import json

# ######## LOCAL ENV ##############
# from dotenv import load_dotenv, find_dotenv

# #Connecting with GCP
# env_path = find_dotenv()
# load_dotenv(env_path)
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# GOOGLE_CX = os.getenv('GOOGLE_CX')
# CREDENTIALS_JSON_GOOGLE_CLOUD = os.getenv('CREDENTIALS_JSON_GOOGLE_CLOUD')

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CX = os.environ.get('GOOGLE_CX')
CREDENTIALS_JSON_GOOGLE_CLOUD = os.environ.get('CREDENTIALS_JSON_GOOGLE_CLOUD')

###############################
###### Google Vision API ######
###############################
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision

    # Google Authentication
    credentials = service_account.Credentials.from_service_account_info(json.loads(CREDENTIALS_JSON_GOOGLE_CLOUD))

    client = vision.ImageAnnotatorClient(credentials=credentials)
    image=vision.Image()
    image.source.image_uri=path

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return response



###############################
###### Text preprocessor ######
###############################
def strip(response):
    # remove these chars from entry
    chars_to_remove = '0123456789!"\'#$%&()*+,-./:;<=>?@[\]^_`{|}~♦●★‒…£¡™¢∞§¶•ªº–≠≠œ∑´®†¥¨≤≥÷ç√€'

    # remove entry if it exactly matches any of these
    drop_exact_words = ['sandwiches','restaurant','menu',
                        'restaurant menu','thank you','drinks',
                        'appetizer','appetizers','mains','dessert',
                        'side','sides','side order','breakfast','lunch'
                       'dinner','supper','starter','starters','local',
                        'fresh','food','main','your','logo','brand name']

    # remove these words from entry
    words_to_remove = ['menu','restaurant','price','appetizer',
                       'appetizers','course','price','extra','extras']

    # remove entry if it contains any of these
    drop_contain_words = ['tax','consumer','advisory','illness','facebook','instagram']

    # remove entry if it starts with any of these
    drop_start_words = ['add','include','includes','including','lorem','with','and',
                       'served','serve']

    # drop entry if it contains fewer chars than minimum
    min_length = 4


    text = response.text_annotations[0].description
    menu_original = text.split('\n')

    menu_chars_removed = []
    for item in menu_original:
        for char in chars_to_remove:
            item = item.replace(char,' ')
        menu_chars_removed.append(item)

    menu_exact_matches_dropped = []
    for item in menu_chars_removed:
        if item.lower() in drop_exact_words:
            pass
        else:
            menu_exact_matches_dropped.append(item)

    menu_words_removed = []
    for item in menu_exact_matches_dropped:
        temporary = []
        for word in item.split(' '):
            if word.lower() not in words_to_remove:
                temporary.append(word)
        remaining_words = ' '.join(temporary)
        menu_words_removed.append(remaining_words)

    menu_contains_dropped = []
    for item in menu_words_removed:
        temporary = []
        for word in item.split(' '):
            if word.lower() in drop_contain_words:
                temporary = []
                pass
            else:
                temporary.append(word)
        remaining_words = ' '.join(temporary)
        menu_contains_dropped.append(remaining_words)

    menu_starts_dropped = []
    for item in menu_contains_dropped:
        temporary = item.split(' ')
        if temporary[0].lower() in drop_start_words:
            pass
        else:
            menu_starts_dropped.append(item)

    menu_exact_matches_dropped = []
    for item in menu_starts_dropped:
        if item.lower() in drop_exact_words:
            pass
        else:
            menu_exact_matches_dropped.append(item)

    bounding_white_space_removed = [item.strip() for item in menu_exact_matches_dropped]
    too_short_dropped = [item for item in bounding_white_space_removed if len(item) >= min_length]

    duplicates_dropped = []
    for item in too_short_dropped:
        if item not in duplicates_dropped:
            duplicates_dropped.append(item)


    stripped_menu = duplicates_dropped

    print(menu_original)
    return(stripped_menu)


##################################
######   Image Search API   ######
##################################

def search_image(query):
    from google_images_search import GoogleImagesSearch
    from google.cloud import vision

    print(f'searching for {query}...')
    print()

    gis = GoogleImagesSearch(GOOGLE_API_KEY,GOOGLE_CX)

    _search_params = {
    'q': f'{query} recipe',
    'num': 1,
    #'imgSize': 'large',
    'imgType': 'photo',
    'imgColorType': 'color'}

    gis.search(search_params=_search_params)
    print('fetching image:')
    if len(gis.results()) == 0:
        print('no image found, not verified as food.')
        print()
        return None

    url = gis.results()[0].url
    print(url)
    print()

    verified_queries = ['cheeseburger','burger','pizza','fried chicken','ice cream sundae','fuyung hai']

    if query.lower() in verified_queries:
        print(f'{query} already in known foods database, no need to verify!')
        print()
        return url

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = url

    response = client.label_detection(image=image, max_results=1)
    label = [lab.description for lab in response.label_annotations]
    score = [lab.score for lab in response.label_annotations]

    text_response = client.text_detection(image=image)
    texts = text_response.text_annotations
    n_chars = 0
    if len(texts)>0:
        n_chars = len(texts[0].description)

    print('verification filter:')
    print('label must be Food or Tableware')
    print('score must be above .96')
    print('number of chars must be below 100')
    print()
    print(f'label: {label}')
    print(f'label score: {score}')
    print(f'chars detected: {n_chars}')
    print()

    try:
        if (label[0] == 'Food' or label[0] == 'Tableware') and score[0] > .96 and n_chars < 100:
            print('verified as food!')
            print()
            print(url)
            print()
            return url
    except IndexError:
        print('label missing, not verified as food')
        pass

    _search_params = {
    'q': f'{query} recipe',
    'num': 3,
    #'imgSize': 'large',
    'imgType': 'photo',
    'imgColorType': 'color',
    'safe': 'medium'}

    gis = GoogleImagesSearch(GOOGLE_API_KEY,GOOGLE_CX)
    gis.search(search_params=_search_params)
    urls = [result.url for result in gis.results()]
    print('fetching additional images:')
    if len(urls)<=1:
        print('no additional images found, not verified as food')
        return None
    urls = urls[1:]
    for url in urls:
        print(url)
    print()

    labels = []
    scores = []
    char_counts = []
    for url in urls:

        image.source.image_uri = url
        response = client.label_detection(image=image, max_results=1)
        label = [lab.description for lab in response.label_annotations]
        score = [lab.score for lab in response.label_annotations]
        labels.append(label)
        scores.append(score)

        text_response = client.text_detection(image=image)
        texts = text_response.text_annotations
        n_chars = 0
        if len(texts)>0:
            n_chars = len(texts[0].description)
        char_counts.append(n_chars)

    print(f'labels: {labels}')
    print(f'label scores: {scores}')
    print(f'chars detected: {char_counts}')
    print()

    for label,score,n_chars in zip(labels,scores, char_counts):
        try:
            if (label[0] == 'Food' or label[0] == 'Tableware') and score[0] > .96 and n_chars < 100:
                print('verified as food!')
                print()
                print(urls[labels.index(label)])
                print()
                return urls[labels.index(label)]
        except:
            pass

    print('not verified as food.')
    print()
    return None



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

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]
