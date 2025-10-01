from sqlmodel import create_engine, Field, SQLModel

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=3)
    headquarters: str

engine = create_engine("sqlite:///D:/Habatik/database.db", echo=True)

SQLModel.metadata.create_all(engine)