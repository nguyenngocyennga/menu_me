import menu_me
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
    img_file_buffer='https://storage.googleapis.com/menu_me_bucket/img.jpg'
    text = detect_text(img_file_buffer)
    text_clean= strip(text)
    text_clean_url=search_image(text_clean)
    text_clean_translated=translate_text(text_clean)
    final_menu ={
            'dish_name': text_clean,
            'img_url': text_clean_url,
            'translated_name': text_clean_translated
                }
    return final_menu
