from sqlmodel import Field, Session, SQLModel, create_engine, select, JSON
from sqlalchemy import text
from tables import Meal

postgres_url = "postgresql://postgres:test123@localhost:5432/recipez"

engine = create_engine(postgres_url, echo=False)


def checkMealTable(item_check):
    with Session(engine) as session:
        query = select(Meal).where(Meal.name == item_check)
        result = session.exec(query).first()
        
        if result is not None:
            print(f"Ingredient '{item_check}' exists in the database")
            return result
        else:
            print("Does not exist in db")
    
if __name__ == "__main__":
    checkMealTable("Sub Salad")