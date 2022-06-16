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
from google.cloud import storage
import json
from google.cloud import vision
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import requests
from itertools import combinations
from statistics import stdev
import six
from google.cloud import translate_v2 as translate

############################## LOCAL ENV ################################
# from dotenv import load_dotenv, find_dotenv

# #Connecting with GCP
# env_path = find_dotenv()
# load_dotenv(env_path)
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# GOOGLE_CX = os.getenv('GOOGLE_CX')
# CREDENTIALS_JSON_GOOGLE_CLOUD = os.getenv('CREDENTIALS_JSON_GOOGLE_CLOUD')

############################## CLOUD RUN ENV #############################
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
    chars_to_remove = '0123456789!"\'#$%&()*+,-./:;<=>?@[\]^_`{|}~♦●★‒…£¡™¢∞§¶•ªº–≠≠œ∑´®†¥¨≤≥÷ç√€。'

    # remove entry if it exactly matches any of these
    drop_exact_words = ['sandwiches','restaurant','menu', 'rooftop', 
                        'restaurant menu','thank you','drinks',
                        'appetizer','appetizers','mains','dessert',
                        'side','sides','side order','breakfast','lunch'
                       'dinner','supper','starter','starters','local',
                        'fresh','food','main','your','logo','brand name'
                       'monday','tuesday','wednesday','thursday','friday',
                       'saturday','sunday','coca cola cola','ooftop','two slice toast  frill chicken  ice berg  tomato slice', 
                        'mozzarella cheese serve with French fries and chili', 'tomato sauce','White bun  beef patty  lettuce  tomato  cheese', 'BBQ sauce  pork bacon  and french fries',
                        'Stir fry noodle with veggie  chicken satay  and', 'fried egg on top and crackers','Stir fry rice with veggie  chicken satay  and fried', 'egg on top with crackers','Grill chicken leg serve with sayur kalasan  rice',
                        'Grill chicken satay serve with rice  crackers','seaduction','best of british café','maishnasons',
                        'profiles', 'tab window', 'help', 'blessing', 'g search or type url']
    
    drop_exact_words = [item.lower() for item in drop_exact_words]

    
    # remove these words from entry
    words_to_remove = ['menu','restaurant','price','appetizer',
                       'appetizers','course','price','extra','extras', 'k']

    # remove entry if it contains any of these
    drop_contain_words = ['tax','consumer','advisory','illness','facebook','instagram']
    
    # remove entry if it starts with any of these
    drop_start_words = ['add','include','includes','including','lorem','with','and',
                       'served','serve']
    
    # drop entry if it contains fewer chars than minimum
    min_length = 4
    
    
    text = response.text_annotations[0].description
    menu_original = text.lower()
    menu_original = menu_original.split('\n')
    
    menu_chars_removed = []
    for item in menu_original:
        for char in chars_to_remove:
            item = item.replace(char,' ')
        menu_chars_removed.append(item)
    menu_chars_removed = [item.strip() for item in menu_chars_removed]
      
    menu_exact_matches_dropped = []
    for item in menu_chars_removed:
        if item.lower() in drop_exact_words:
            pass
        else:
            menu_exact_matches_dropped.append(item)
    menu_exact_matches_dropped = [item.strip() for item in menu_exact_matches_dropped]
        
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
    
    print('original menu:')
    print()
    print(menu_original)
    print()
    print('stripped menu:')
    print()
    print(stripped_menu)
    print()
    return stripped_menu


##################################
######   Image Search API   ######
##################################

def search_image(query):
    helper_word = 'recipe'
    
    bev_cv = pd.read_csv('data/stripped_drinks.csv')
    beverages = bev_cv['name'].tolist()
    beverages += ['coca cola', 'cola', 'pepsi','coffee','pepsi cola','bintang',
                  'budweiser','red wine', 'mountain dew','coke','screwdriver', 'red bull', 'redbull', 'starbucks coffee']

    if query.lower() in beverages:
        helper_word = 'beverage'
    
    print(f'searching for {query} ({helper_word})...')
    print()

    gis = GoogleImagesSearch(GOOGLE_API_KEY,GOOGLE_CX)

    if query.lower() in beverages:
        helper_word = 'beverage'
    
    _search_params = {
    'q': f'{query} {helper_word}',
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
    
    verified_queries = ['cheeseburger','burger','pizza','fried chicken','ice cream sundae','fuyung hai','screwdriver','redbull',
                       'loaded baked potato', 'roasted vegetables','strawberry cake','hamburger','subway','potato chips','french fries','salad',
                       'coca cola', 'pepsi cola', 'redbull', 'red bull','mountain dew','starbucks coffee','baskin robbins sundae','chicken burger',
                        'grill chicken sandwich','beef burger','singapore fried noodle','fried rice','ayam bakar taliwang','chicken satay']
    
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
    print('label must be Food, Tableware, Bottle, Beverage can, Liquid, or Water')
    print('score must be above .955')
    print('number of chars must be below 200')
    print()
    print(f'label: {label}')
    print(f'label score: {score}')
    print(f'chars detected: {n_chars}')
    print()
    
    try:
        if (label[0] in ['Food','Tableware','Bottle','Beverage can','Liquid','Water']) and score[0] > .955 and n_chars < 200:
            print('verified!')
            print()
            print(url)
            print()
            return url
    except IndexError:
        print('label missing, not verified.')
        pass
    

    _search_params = {
    'q': f'{query} {helper_word}]',
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
        print('no additional images found, not verified.')
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
            if (label[0] in ['Food','Tableware','Bottle','Beverage can','Liquid','Water']) and score[0] > .955 and n_chars < 200:
                print('verified!')
                print()
                print(urls[labels.index(label)])
                print()
                return urls[labels.index(label)]
        except:
            pass
        
    print('not verified.')
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
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    dish_translated =result["translatedText"]
    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return dish_translated


################################################
######            Menu annotation         ######
################################################
def get_language(response):
    language = response.text_annotations[0].locale
    print('language:')
    print(language)
    print()
    return language


def detect_text_points(response):
    
    chars_to_remove = '0123456789!"\'#$%&()*+,-./:;<=>?@[\]^_`{|}~♦●★‒…£¡™¢∞§¶•ªº–≠≠œ∑´®†¥¨≤≥÷ç√€。'
    
    texts = response.text_annotations
    language = texts[0].locale

    text_list = []
    location_list = []

    for text in texts[1:]:
        new_text = '''{}'''.format(text.description)
        text_list.append(new_text)
        
        vertices = [tuple((vertex.x, vertex.y)) for vertex in text.bounding_poly.vertices]
        
        location_list.append(vertices[0])
        
    detected_df = pd.DataFrame({
        'text': text_list,
        'location': location_list})

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    if language in ['zh','zh-hk','zh-cn','zh-sg','zh-tw','ja','ko']:
        split_chars = []
        for item in detected_df.text:
            split_chars.append([char for char in item])
        
        detected_df['text'] = split_chars
        detected_df = detected_df.explode('text')
    
    for char in chars_to_remove:
        detected_df = detected_df[detected_df['text'] != char]

    detected_df['text'] = detected_df['text'].str.lower()
    print(detected_df)
    print()
        
    return detected_df


def detect_item_locations(detected_df, stripped_menu, language='en'):    
    if language in ['ar','iw','fa','ur','sd','ps','yi']:
        box_dict = dict()
        for item in stripped_menu:
            box_dict[item] = None
        print(box_dict)
        print()
        return box_dict
    
    if language in ['zh','zh-hk','zh-cn','zh-sg','zh-tw','ja','ko'] and len(detected_df)>110:
        box_dict = dict()
        for item in stripped_menu:
            box_dict[item] = None
        print(box_dict)
        print()
        return box_dict

    split_items = []
    if language in ['zh','zh-hk','zh-cn','zh-sg','zh-tw','ja','ko']:
        for item in stripped_menu:
            split_items.append([char for char in item])
            
    else:
        for item in stripped_menu:
            split_items = [item.split() for item in stripped_menu]
    

    final_item_locations = dict()
    all_items_dfs = []
    for item in split_items:
        item_df = pd.DataFrame()
        for word in item:
            mask = detected_df['text'] == word
            item_df = pd.concat([item_df, detected_df[mask]])
            item_df = item_df.drop_duplicates()
        all_items_dfs.append(item_df)
        
        word_locations = list(zip(item_df.text, item_df.location))
        
        combos = []
        
        for combo in list(combinations(word_locations, len(item))):
            word = [pair[0] for pair in combo]
            if len(set(word)) == len(item):
                combos.append(combo)
                
        calc_df = pd.DataFrame(combos)
      
        location_stds =  []
        for combo in combos:
            location = [pair[1] for pair in combo]

            if len(location) >=2:
                calc_nums = [pair[1] for pair in location]
                location_stds.append(stdev(calc_nums))
            else:
                location_stds.append(0)
        calc_df['location_stds'] = location_stds
        calc_df = calc_df.sort_values(by=['location_stds'])
        
        if len(calc_df) > 0:
            calc_df = calc_df.iloc[[0]]
        
        item_full_info = []
        for column in calc_df:
            if column != 'location_stds':
                item_full_info.append(calc_df[column].to_string(index=False))

        item_name = []
        item_location = []
        for item in item_full_info:
            pair = item.split(', ')
            
            name = [char for char in pair[0] if char not in '[](),']
            name = ''.join(name)
            item_name.append(''.join(name))
            
            location = [char for char in pair [1:]]
            location = str(location)
            location = [char for char in location if char in string.digits or char not in string.punctuation]
            location = ''.join(location)
            location = location.split(' ')
            location = [int(n) for n in location]
            item_location.append(location)
            
        item_name = ' '.join(item_name)
        if len(item_location) > 0:
            final_item_locations[item_name] = item_location[0]
            
    for item_name in stripped_menu:
        if item_name not in final_item_locations.keys():
            final_item_locations[item_name] = None
        
    print(final_item_locations)
    return final_item_locations

def show_menu_markers(path, coord_dict, count):
    response = requests.get(path)
    img = Image.open(BytesIO(response.content))

    plt.figure(figsize=(10, 20))
    plt.axis("off")
    plt.imshow(img)
    
    for value in coord_dict.values():
        plt.scatter(x = value[0], y = value[1], alpha=.6, marker ="*", c='red', edgecolors='blue', s=1500)
    
    
    unique_name = path.split('/')[-1].split('.')[0]
    base_url = "data/menu_star_temp"
    item_name = list(coord_dict.keys())[0].replace(" ", "-").lower()
    cloud_filename = f'{count}_{unique_name}_{item_name}.png'
    full_local_path = f"{base_url}/{cloud_filename}"
    plt.savefig(full_local_path, bbox_inches='tight')
    plt.close()

    credentials = service_account.Credentials.from_service_account_info(json.loads(CREDENTIALS_JSON_GOOGLE_CLOUD))
    client = storage.Client(credentials=credentials, project='menu-me-352703')
    bucket = client.get_bucket('menu_me_bucket')
    blob = bucket.blob(cloud_filename)
    blob.upload_from_filename(full_local_path)

    menu_star_url = f"https://storage.googleapis.com/menu_me_bucket/{cloud_filename}"
    print(menu_star_url)

    path = base_url
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                os.unlink(os.path.join(path, entry.name))

    return menu_star_url
