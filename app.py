import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

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

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # st.write(type(img_array))
    # st.write(img_array.shape)
    display_menu(sample_data)
