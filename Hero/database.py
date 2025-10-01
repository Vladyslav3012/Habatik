from sqlmodel import create_engine, Field, SQLModel
from Team.database import Team

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=3)
    secret_name: str
    age: int|None = Field(default=None, index=True, ge=1, le=120)

    team_id: int | None = Field(default=None, foreign_key="team.id")

engine = create_engine("sqlite:///D:/Habatik/database.db", echo=True)

SQLModel.metadata.create_all(engine)
