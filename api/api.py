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
def api_get_all_dishnames(path):
    text = detect_text(path)
    text_clean= strip(text)
    return text_clean

@app.get("/item")
def api_item_details(item,target='en'):
    img_url = search_image(item)
    translated_name = translate_text(target=target, text=item)
    print('')
    print('Original Dish Name: ', item)
    print('Image Url: ', img_url)
    print('Translated Name: ', translated_name)

    full_item = {
            'dish_name': item,
            'img_url': img_url,
            'translated_name': translated_name
                }
    return full_item
