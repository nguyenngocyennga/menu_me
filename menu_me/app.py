import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import base64
from io import BytesIO
import string

#img_file_buffer = st.camera_input("Take a picture!")

# sample_data = pd.DataFrame({
#     'dish_name': ['Nasi Goreng', 'Mie Goreng'],'img_url': ["https://cdn1-production-images-kly.akamaized.net/KxuztQKl3tnUN0Fw5iAwKsnX_u0=/0x148:1920x1230/640x360/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/3093328/original/069244600_1585909700-fried-2509089_1920.jpg", "https://cdn0-production-images-kly.akamaized.net/ocS8U9pjo2A1EDhgmyvw1Deo8Ko=/469x260/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3129172/original/099632200_1589527804-shutterstock_1455941861.jpg"],
#     'translated_name': ['Fried Rice', 'Fried Noodles']
# })

def display_menu(df):
    for index, row in df.iterrows():
        st.image(row['img_url'], use_column_width='always')
        st.title(row['dish_name'])
        st.subheader(row['translated_name'])


###############################
###### Google Vision API ######
###############################
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    #content = x
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations[0]
    #print('Texts:')

    #print(('\n"{}"'.format(texts.description)))

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
def translate_text(text, target):
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



###############################
######   Streamlit Test   #####
###############################

# if img_file_buffer is not None:
#     # To read image file buffer as a PIL Image:
#     img = Image.open(img_file_buffer)
#     st.write(type(img))
#     rgb_im = img.convert("RGB")
#     rgb_im.save("img.jpg")
#     #converted_pic=encode_image(rgb_im)

#     # To convert PIL Image to numpy array:
#     img_array = np.array(img)

#     raw_output = detect_text("img.jpg")
#     cleaned_text = strip(raw_output)
    # st.write(cleaned_text)

#     all_dishes_url = []
#     all_dishes_translation = []
#     for item in cleaned_text:
#         img_url = search_image(item)
#         all_dishes_url.append(img_url)
#         translated_text = translate_text(target, item)
#         all_dishes_translation.append(translated_text)

#     final_menu = pd.DataFrame(
#         {
#             'dish_name': cleaned_text,
#             'img_url': all_dishes_url,
#             'translated_name': all_dishes_translation
#         }
#     )

    # print(cleaned_text)
    # print(all_dishes_url)
    # print(all_dishes_translation)
    # print('#############')
    # print(final_menu)


    # display_menu(final_menu)
