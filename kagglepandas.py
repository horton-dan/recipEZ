import pandas as pd
import ast

# Load the CSV file
df = pd.read_csv('KaggleRecipes/RAW_recipes.csv')

# Isolate just the ingredients column
ingredients = df['ingredients']

# Get the ingredients string from the first row
ingredients_str = df.loc[0, 'ingredients']
print("Raw ingredients string:", ingredients_str)

# Convert string representation of list to actual list using ast.literal_eval
ingredients_list = ast.literal_eval(ingredients_str)


# To process all rows, you can do:
# for index, row in df.iterrows():
#     ingredients_list = ast.literal_eval(row['ingredients'])
#     for individual_ingredient in ingredients_list:
#         print(individual_ingredient)






