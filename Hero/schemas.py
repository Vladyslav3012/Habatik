from pydantic import BaseModel

class HeroSearch(BaseModel):
    name: str|None = None
    secret_name: str | None = None
    age: int | None = None