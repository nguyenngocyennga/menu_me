
sample_data = pd.DataFrame({
    'dish_name': ['Nasi Goreng', 'Mie Goreng', 'Nasi Goreng', 'Mie Goreng'],
    'img_url': ["https://cdn1-production-images-kly.akamaized.net/KxuztQKl3tnUN0Fw5iAwKsnX_u0=/0x148:1920x1230/640x360/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/3093328/original/069244600_1585909700-fried-2509089_1920.jpg", "https://cdn0-production-images-kly.akamaized.net/ocS8U9pjo2A1EDhgmyvw1Deo8Ko=/469x260/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3129172/original/099632200_1589527804-shutterstock_1455941861.jpg", "https://cdn1-production-images-kly.akamaized.net/KxuztQKl3tnUN0Fw5iAwKsnX_u0=/0x148:1920x1230/640x360/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/3093328/original/069244600_1585909700-fried-2509089_1920.jpg", "https://cdn0-production-images-kly.akamaized.net/ocS8U9pjo2A1EDhgmyvw1Deo8Ko=/469x260/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3129172/original/099632200_1589527804-shutterstock_1455941861.jpg"],
    'translated_name': ['Fried Rice', 'Fried Noodles', 'Fried Rice', 'Fried Noodles']
})

###############################
######## Display menu #########
###############################
def display_menu(df):
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
