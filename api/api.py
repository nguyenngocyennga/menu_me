from menu_me.app import detect_text, strip, search_image, translate_text
from menu_me.ingredient_function import find_ingredients
from menu_me.recipe_function import find_recipe
from menu_me.allergy_function import allergy_check
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
def api_function(path):
    text = detect_text(path)
    text_clean= strip(text)

    text_clean_url=[]
    text_clean_translated=[]
    for item in text_clean:
        img_url = search_image(item)
        text_clean_url.append(img_url)
        translated_name = translate_text(target='en', text=item)
        text_clean_translated.append(translated_name)
        allergy = allergy_check(translated_name)
        recipe = find_recipe(translated_name)
        ingredients = find_ingredients(translated_name)
        print('')
        print('Original Dish Name:: ', item)
        print('Image Url: ', img_url)
        print('Translated Name: ', translated_name)
        print('allergy:', allergy)
        print('recipe', recipe )
        print('ingredients:', ingredients )

    final_menu ={
            'dish_name': text_clean,
            'img_url': text_clean_url,
            'translated_name': text_clean_translated,
            'allergy_information': allergy,
            'recipe': recipe,
            'ingredients:': ingredients
                }
    print('############################################')
    print('###   API is successfully constructed!   ###')
    print('############################################')
    return final_menu
