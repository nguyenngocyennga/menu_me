import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import base64
from io import BytesIO
import string

img_file_buffer = st.camera_input("Take a picture!")  

sample_data = pd.DataFrame({
    'dish_name': ['Nasi Goreng', 'Mie Goreng'],'img_url': ["https://cdn1-production-images-kly.akamaized.net/KxuztQKl3tnUN0Fw5iAwKsnX_u0=/0x148:1920x1230/640x360/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/3093328/original/069244600_1585909700-fried-2509089_1920.jpg", "https://cdn0-production-images-kly.akamaized.net/ocS8U9pjo2A1EDhgmyvw1Deo8Ko=/469x260/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3129172/original/099632200_1589527804-shutterstock_1455941861.jpg"],
    'translated_name': ['Fried Rice', 'Fried Noodles']
})

def display_menu(df):
    for index, row in df.iterrows():
        st.image(row['img_url'], use_column_width='always')
        st.title(row['dish_name'])
        st.subheader(row['translated_name'])


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

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    raw_output = detect_text("img.jpg")
    cleaned_text = strip(raw_output)
    st.write(cleaned_text)
    
    # Image API for cleaned_text
    
    
    # Translation API for cleaned_text
    
    
    # Display menu in streamlit
    display_menu(sample_data)

