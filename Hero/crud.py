from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException
from typing import List

from Habatik.Hero.schemas import HeroSearch
from Habatik.Hero.database import engine, Hero

router = APIRouter(tags=['Heroes'], prefix='/heroes')

@router.post('/newHero')
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return {"New hero": hero}


@router.get("/allHero", response_model=List[Hero])
def get_all_hero():
    with Session(engine) as session:
        statement = select(Hero)
        result = session.exec(statement)
        return result.all()


@router.get("/{hero_id}", response_model=Hero)
def get_hero_by_id(hero_id: int):
    with Session(engine) as session:
        result = session.get(Hero, hero_id)
        if not result:
            raise HTTPException(status_code=404, detail="Hero not found")
        return result


@router.put('/uptade/{hero_id}')
def update_hero_by_id(hero_id: int, data_for_update: HeroSearch):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="hero not found")
        if not data_for_update:
            raise HTTPException (status_code=404, detail="Please send data for update")
        if data_for_update.name:
            hero.name = data_for_update.name
        if data_for_update.secret_name:
            hero.secret_name = data_for_update.secret_name
        if data_for_update.age:
            hero.age = data_for_update.age

        session.add(hero)
        session.commit()
        session.refresh(hero)

        return {"Hero update": hero}


@router.delete("/delete")
def delete_hero(hero:HeroSearch):
    with Session(engine) as session:
        if hero.name:
            statement = select(Hero).where(Hero.name == hero.name)
            filter_field, value = "name", hero.name
        elif hero.secret_name:
            statement = select(Hero).where(Hero.secret_name == hero.secret_name)
            filter_field, value = "secret_name", hero.secret_name
        elif hero.age:
            statement = select(Hero).where(Hero.age == hero.age)
            filter_field, value = "age", hero.age
        else: raise HTTPException(status_code=404, detail="Provide data")

        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(result)
        session.commit()
        return {"Status": "success", "delete_by": filter_field, "value": value}

