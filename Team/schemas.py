from pydantic import BaseModel

class TeamSearch(BaseModel):
    name: str | None = None
    headquarters: str | None = None