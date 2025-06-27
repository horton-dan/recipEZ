from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import JSON
import pandas as pd
import ast
import os.path
from dotenv import load_dotenv

load_dotenv

class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ingredient_name: str

class Meal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    ingredients: dict = Field(sa_type=JSON)

postgres_url = os.getenv('postgres_url')

engine = create_engine(postgres_url, echo=False)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

def add_ingredients():
    print("Enter ingredients (one per line). Press Enter twice to finish:")
    ingredients = []
    while True:
        ingredient_name_input = input("> ").strip()
        if not ingredient_name_input:  # If user enters empty line
            break
        ingredients.append(Ingredient(ingredient_name=ingredient_name_input))
    
    if ingredients:  # Only proceed if there are ingredients to add
        with Session(engine) as session:
            session.add_all(ingredients)
            session.commit()
            print(f"Added {len(ingredients)} ingredients successfully!")
    else:
        print("No ingredients were added.")
def ingredientCSV_database():

    # Load the CSV file
    df = pd.read_csv('KaggleRecipes/RAW_recipes.csv')

    # Isolate just the ingredients column
    ingredients = df['ingredients']

    for ingredient_list_row in range(len(ingredients)):
        ingredient_string = df.loc[ingredient_list_row, 'ingredients']
        #Convert to a Python literal String
        ingredient_list = ast.literal_eval(ingredient_string)
        for individual_ingredient in ingredient_list:
            with Session(engine) as session:
                session.add(Ingredient(ingredient_name=individual_ingredient))
                session.commit()
            

def create_meal():    
    meal_ingredients = []
    meal_name_input = input("Please enter a name for the meal: ").strip()
    #Add ingredients that make a meal
    while True:
        meal_ingredient_input = input("> ").strip()
        if not meal_ingredient_input:
            break
        with Session(engine) as session:
            ingredient_check = session.exec(select(Ingredient).where(Ingredient.ingredient_name == meal_ingredient_input)).first()
            if ingredient_check:
                meal_ingredients.append(meal_ingredient_input)
            else:
                print("Ingredient does not exist.")        

    ingredient_dict = {"ingredients" : meal_ingredients}

    if meal_ingredients:  # Only proceed if there are ingredients to add
        with Session(engine) as session:
            session.add(Meal(name=meal_name_input,ingredients=ingredient_dict))
            session.commit()
            print(f"Added successfully!")
    else:
        print("No meal was added.")

def select_testing():
    with Session(engine) as session:
        show_ingredients = session.exec(select(Ingredient).where(Ingredient.ingredient_name == "Brats")).first()
        #This is how you show the results to console
        # for ingredients in show_ingredients:
        #     print(ingredients)
        if show_ingredients:
            print("Exists")
        else:
            print("Does not exist")
if __name__ == "__main__":
    # add_ingredients()
    create_meal()    
    # create_db_tables()
    # select_testing()
    # ingredientCSV_database()