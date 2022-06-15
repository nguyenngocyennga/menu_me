import pandas as pd
from difflib import get_close_matches
food_df = pd.read_csv('data/ruben_food_data.csv')



#test 2.0
#testing --> dish_translated="fried rice"

def allergy_check(dish_translated):
    # define a list of common allergies
    common_allergens_list_cowsmilk=['cheese','parmesan','butter','margarine','yogurt','cream','ice cream','milk','milk powder']
    common_allergens_list_eggs=['egg', 'omelette']
    common_allergens_list_treenuts=['brazil nut', 'almond', 'cashew', 'macadamia nut','pistachio','pine nut','walnut']
    common_allergens_list_peanuts=['peanut']
    common_allergens_list_shellfish=['shrimp','prawn','crayfish', 'lobster','squid','scallops']
    common_allergens_list_wheat=['wheat', 'pasta','noodle','bread','crust','flour']
    common_allergens_list_soy=['soy','tofu','soya','soybean']
    common_allergens_list_fish=['fish','seafood']
    # define an empty list for the allergy check
    true_or_false_cowsmilk=[]
    true_or_false_eggs=[]
    true_or_false_treenuts=[]
    true_or_false_peanuts=[]
    true_or_false_shellfish=[]
    true_or_false_wheat=[]
    true_or_false_soy=[]
    true_or_false_fish=[]

    # if {dish_translated} is empty
    if dish_translated=="":
        return 'There was no dish input'

    # if {dish_translated} is an exact match
    if len(food_df[food_df['Title']==dish_translated]) != 0:
        pot_food_df = food_df[food_df['Title']==dish_translated]

        possible_allergies= []
        # Cowsmilk
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_cowsmilk.append(any(ele in row for ele in common_allergens_list_cowsmilk))
        if True in true_or_false_cowsmilk:
            possible_allergies.append('cowsmilk')

        # Eggs
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_eggs.append(any(ele in row for ele in common_allergens_list_eggs))
        if True in true_or_false_eggs:
            possible_allergies.append('eggs')

        # Tree nuts
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_treenuts.append(any(ele in row for ele in common_allergens_list_treenuts))
        if True in true_or_false_treenuts:
            possible_allergies.append('treenuts')

        # Peanuts
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_peanuts.append(any(ele in row for ele in common_allergens_list_peanuts))
        if True in true_or_false_peanuts:
            possible_allergies.append('peanuts')

        # Shellfish
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_shellfish.append(any(ele in row for ele in common_allergens_list_shellfish))
        if True in true_or_false_shellfish:
            possible_allergies.append('shellfish')

        # Wheat
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_wheat.append(any(ele in row for ele in common_allergens_list_wheat))
        if True in true_or_false_wheat:
            possible_allergies.append('wheat')

        # Soy
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_soy.append(any(ele in row for ele in common_allergens_list_soy))
        if True in true_or_false_soy:
            possible_allergies.append('soy')

        # Fish
        for row in pot_food_df['Cleaned_Ingredients']:
            true_or_false_fish.append(any(ele in row for ele in common_allergens_list_fish))
        if True in true_or_false_fish:
            possible_allergies.append('fish')

        if len(possible_allergies) != 0:
            return possible_allergies
        else:
            return 'This dish has most likely no ingredients that are known to our allergenes list'


        ###########################################################################################

    # if it is not an exact match
    else:
        pot_food_df=food_df[food_df['Title'].str.contains(dish_translated, na=False)]

        closest_dishes=(get_close_matches('{dish_translated}', list(pot_food_df['Title']),n=5,cutoff=0.01))

        #look for the 5 dishes in the pot_food_df and return them - in a --> DF/a list of ingredients
        list_of_ingredients=[]
        for i in closest_dishes:
            ingredi=pot_food_df.loc[pot_food_df['Title']==i]['Cleaned_Ingredients'].tolist()
            list_of_ingredients.append(ingredi)


        possible_allergies= []
        # Cowsmilk
        for row in list_of_ingredients:
            true_or_false_cowsmilk.append(any(ele in row[0] for ele in common_allergens_list_cowsmilk))
        if True in true_or_false_cowsmilk:
            possible_allergies.append('cowsmilk')


        # Eggs
        for row in list_of_ingredients:
            true_or_false_eggs.append(any(ele in row[0] for ele in common_allergens_list_eggs))
        if True in true_or_false_eggs:
            possible_allergies.append('eggs')


        # Tree nuts
        for row in list_of_ingredients:
            true_or_false_treenuts.append(any(ele in row[0] for ele in common_allergens_list_treenuts))
        if True in true_or_false_treenuts:
            possible_allergies.append('treenuts')


        # Peanuts
        for row in list_of_ingredients:
            true_or_false_peanuts.append(any(ele in row[0] for ele in common_allergens_list_peanuts))
        if True in true_or_false_peanuts:
            possible_allergies.append('peanuts')


        # Shellfish
        for row in list_of_ingredients:
            true_or_false_shellfish.append(any(ele in row[0] for ele in common_allergens_list_shellfish))
        if True in true_or_false_shellfish:
            possible_allergies.append('shellfish')


        # Wheat
        for row in list_of_ingredients:
            true_or_false_wheat.append(any(ele in row[0] for ele in common_allergens_list_wheat))
        if True in true_or_false_wheat:
            possible_allergies.append('wheat')

        # Soy
        for row in list_of_ingredients:
            true_or_false_soy.append(any(ele in row[0] for ele in common_allergens_list_soy))
        if True in true_or_false_soy:
            possible_allergies.append('soy')


        # Fish
        for row in list_of_ingredients:
            true_or_false_fish.append(any(ele in row[0] for ele in common_allergens_list_fish))
        if True in true_or_false_fish:
            possible_allergies.append('fish')



        if len(possible_allergies) != 0:
            return possible_allergies
        else:
            return 'No information found for this dish'


        # if there is no data returned, the dish is not in our database
        if len(pot_food_df)==0:
            return "We do not recoginze this dish"


#allergy_check(dish_translated)
