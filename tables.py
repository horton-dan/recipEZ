from sqlmodel import Field, Session, SQLModel, create_engine, select, JSON
from sqlalchemy import text

class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ingredient_name: str

class Meal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    ingredients: dict = Field(sa_type=JSON)