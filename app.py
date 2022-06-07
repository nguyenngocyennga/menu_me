import streamlit as st
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import string

img_file_buffer = st.camera_input("Take a picture!")


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


chars_to_remove = ''
chars_to_remove += string.punctuation
chars_to_remove += string.digits
chars_to_remove += '$:●★‒…£¡™¢∞§¶•ªº–≠≠œ∑´®†¥¨≤≥÷ç√€'
def strip(raw_text):
#    text = response.text_annotations[0].description
    orig = raw_text.split('\n')
    clean_entries = []
    for entry in orig:
        for char in chars_to_remove:
            entry = entry.replace(char,'')
        clean_entries.append(entry)
    clean_entries = [x for x in clean_entries if len(x)>4]
    print(orig)
    print()
    print(clean_entries)
    return clean_entries

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)
    st.write(type(img))
    rgb_im = img.convert("RGB")
    rgb_im.save("img.jpg")
    #converted_pic=encode_image(rgb_im)

    raw_output = detect_text("img.jpg")
    cleaned_text = strip(raw_output)
    st.write(cleaned_text)
