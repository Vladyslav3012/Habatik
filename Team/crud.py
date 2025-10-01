from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException
from typing import List

from Habatik.Team.schemas import TeamSearch
from Habatik.Team.database import engine, Team

router = APIRouter(tags=['Teams'], prefix='/teams')


@router.post('/newTeam')
def create_team(team: Team):
    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)
        return {"New team": team}

@router.get("/allTeam", response_model=List[Team])
def get_all_team():
    with Session(engine) as session:
        statement = select(Team)
        result = session.exec(statement)
        return result.all()

@router.get("/{team_id}", response_model=Team)
def get_team_by_id(team_id: int):
    with Session(engine) as session:
        result = session.get(Team, team_id)
        if not result:
            raise HTTPException(status_code=404, detail="Team not found")
        return result




@router.put('/uptade/{team_id}')
def update_team_by_id(team_id: int, data_for_update: TeamSearch):
    with Session(engine) as session:
        team = session.get(Team, team_id)
        if not team:
            raise HTTPException(status_code=404, detail="team not found")
        if not data_for_update:
            raise HTTPException(status_code=404, detail="Please send data for update")
        if data_for_update.name:
            team.name = data_for_update.name
        if data_for_update.headquarters:
            team.headquarters = data_for_update.headquarters

        session.add(team)
        session.commit()
        session.refresh(team)

        return {"Team update": team}


@router.delete("/delete")
def delete_team(team: Team):
    with Session(engine) as session:
        if team.name:
            statement = select(Team).where(Team.name == team.name)
            filter_field, value = "name", team.name
        elif team.headquarters:
            statement = select(Team).where(Team.headquarters == team.headquarters)
            filter_field, value = "headquarters", team.headquarters
        else:
            raise HTTPException(status_code=404, detail="Provide data")

        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Team not found")
        session.delete(result)
        session.commit()
        return {"Status": "success", "delete_by": filter_field, "value": value}

