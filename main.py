from fastapi import FastAPI
from Habatik.Hero.crud import router as hero_router
from Habatik.Team.crud import router as team_router

app = FastAPI()
app.include_router(hero_router)
app.include_router(team_router)