from menu_me.app import detect_text, strip, search_image, translate_text, get_language, detect_text_boxes, map_text_boxes, save_one_menu_box
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
def api_get_all_dishnames(path):
    response = detect_text(path)
    language = get_language(response)
    stripped_menu= strip(response)
    detected_df = detect_text_boxes(response)
    box_dict = map_text_boxes(detected_df, stripped_menu, language)
    result = {}

    count = 0
    for key,value in box_dict.items():
        if value != None:
            coord_dict = {key:value}
            result[key] = save_one_menu_box(path, coord_dict, count)
            count += 1
        else:
            result[key] = None
    return result

@app.get("/item")
def api_item_details(item,target='en'):
    img_url = search_image(item)
    translated_name = translate_text(target=target, text=item)
    allergy = allergy_check(translated_name)
    recipe = find_recipe(translated_name)
    ingredients = find_ingredients(translated_name)
    print('')
    print('Original Dish Name: ', item)
    print('Image Url: ', img_url)
    print('Translated Name: ', translated_name)
    print('allergy:', allergy)
    print('recipe', recipe )
    print('ingredients:', ingredients )

    full_item = {
            'dish_name': item,
            'img_url': img_url,
            'translated_name': translated_name,
            'allergy_information': allergy,
            'recipe': recipe,
            'ingredients': ingredients
            }

    return full_item
