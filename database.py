from sqlmodel import Field, Session, SQLModel, create_engine

class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ingredient_name: str

postgres_url = "postgresql://postgres:test123@localhost:5432/recipez"

engine = create_engine(postgres_url, echo=True)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

def create_ingredients():
    ingredient_1 = Ingredient(id=1, ingredient_name="chicken")
    #using the 'with' block means you do not have to mannually use session.close() to close out lingering resources. It handles it for you even if the code breaks during the block.
    with Session(engine) as session:
        session.add(ingredient_1)
        session.commit()
        # session.close()
def main():
    create_db_tables()
    create_ingredients()

if __name__ == "__main__":
    main()
