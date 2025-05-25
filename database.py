from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import JSON


class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ingredient_name: str

class Meal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ingredients: dict = Field(sa_type=JSON)

postgres_url = "postgresql://postgres:test123@localhost:5432/recipez"

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

def create_meal():    
    meal_ingredients = []
    meal_name_input = input("Please enter a name for the meal: ").strip()
    #Add ingredients that make a meal
    while True:
        meal_ingredient_input = input("> ").strip()
        if not meal_ingredient_input:
            break
        meal_ingredients.append(meal_ingredient_input)
    
    meal_dict = {"name" : meal_name_input,
               "ingredients" : meal_ingredients
               }
    
    

    if meal_ingredients:  # Only proceed if there are ingredients to add
        with Session(engine) as session:
            session.add(Meal(ingredients=meal_dict))
            session.commit()
            print(f"Added successfully!")
    else:
        print("No meal was added.")



if __name__ == "__main__":
    add_ingredients()
    create_meal()    
    create_db_tables()
