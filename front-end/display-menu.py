
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
#from google.cloud import storage
import os
from google.oauth2 import service_account
import json
from dotenv import load_dotenv, find_dotenv
from api.api import api_function
#import base64
#from io import BytesIO




###############################
######## Display menu #########
###############################
def display_menu(df):
    df = pd.DataFrame(df)
    with open('front-end/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    for index, row in df.iterrows():
        st.markdown(f'''<div class="card-product">
            <img src="{row['img_url']}"/>
            <div class="card-product-infos">
                <h2>{row['dish_name']}</h2>
                <p>{row['translated_name']}</p>
            </div>
            </div>''', unsafe_allow_html=True)


##################################
####   Streamlit home page    ####
##################################
env_path = find_dotenv()
load_dotenv(env_path)
CREDENTIALS_JSON_GOOGLE_CLOUD = os.getenv('CREDENTIALS_JSON_GOOGLE_CLOUD')


# img_file_buffer = st.camera_input("Take a picture!")

# if img_file_buffer is not None:
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    rgb_im = img.convert("RGB")
    rgb_im.save("img.jpg")
    credentials = service_account.Credentials.from_service_account_info(json.loads(CREDENTIALS_JSON_GOOGLE_CLOUD))
    client = storage.Client(credentials=credentials, project='menu-me-352703')
    bucket = client.get_bucket('menu_me_bucket')
    blob = bucket.blob("img.jpg")
    blob.upload_from_filename("img.jpg")
    st.write('Photo is uploaded 🥳')
    st.write('Your menu is coming soon... 🌮 🌯 🥙')
    df = api_function()
    display_menu(df)
