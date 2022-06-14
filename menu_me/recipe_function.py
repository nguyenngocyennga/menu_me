import pandas as pd
food_df = pd.read_csv('../data_to_include/ruben_food_data.csv')

#################################
#####  Find recipe function  ####
#################################
def find_recipe(dish_translated):
    if dish_translated=="":
        return 'There was no dish input'
    if len(food_df[food_df['Title']==dish_translated]) != 0:
        small_food_df = food_df[food_df['Title']==dish_translated].reset_index()
        ins=small_food_df['Instructions'][0]
        ins=ins.replace('\n', ' ')
        return ins
    else:
        return 'No ingredients found'
#find_recipe('spanakopita')
