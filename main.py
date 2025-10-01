from fastapi import FastAPI
from Hero.crud import router as hero_router
from Team.crud import router as team_router

app = FastAPI()
app.include_router(hero_router)
app.include_router(team_router)