from menu_me.app import detect_text, strip, search_image, translate_text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return dict(greeting="hello")

@app.get("/dish")
def api_function():
    text = detect_text()
    text_clean= strip(text)

    text_clean_url=[]
    text_clean_translated=[]
    for item in text_clean:
        img_url = search_image(item)
        text_clean_url.append(img_url)
        translated_name = translate_text(target='en', text=item)
        text_clean_translated.append(translated_name)
        print('')
        print('Original Dish Name:: ', item)
        print('Image Url: ', img_url)
        print('Translated Name: ', translated_name)

    final_menu ={
            'dish_name': text_clean,
            'img_url': text_clean_url,
            'translated_name': text_clean_translated
                }
    print('############################################')
    print('###   API is successfully constructed!   ###')
    print('############################################')
    return final_menu
