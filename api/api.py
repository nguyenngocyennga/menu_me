from menu_me.app import detect_text
from menu_me.app import strip
from menu_me.app import search_image
from menu_me.app import translate_text
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
        text_clean_url.append(search_image(item))
        text_clean_translated.append(translate_text(target='en', text=item))

    final_menu ={
            'dish_name': text_clean,
            'img_url': text_clean_url,
            'translated_name': text_clean_translated
                }
    return final_menu
