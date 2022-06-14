import pandas as pd
food_df = pd.read_csv('../data/ruben_food_data.csv')

#################################
#### Find ingredient function ###
#################################
def find_ingredients(dish_translated):
    if dish_translated=="":
        return 'There was no dish input'
    if len(food_df[food_df['Title']==dish_translated]) != 0:
        small_food_df = food_df[food_df['Title']==dish_translated].reset_index()
        ing=small_food_df['Cleaned_Ingredients'][0]
        ing=ing.replace( '[' , '')
        ing=ing.replace( ']' , '')
        ing=ing.replace( ' " ' , '')
        return ing
    else:
        return 'No ingredients found'
#find_ingredients('brownie pudding cake')
