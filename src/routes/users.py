from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel
from src.repository import users as repository_users

router = APIRouter(prefix='/users', tags=["users"])


@router.get("/", response_model=List[UserModel])
async def read_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), name: str | None = None,
                     surname: str | None = None, email: str | None = None):
    users = await repository_users.get_users(skip, limit, db, name, surname, email)
    return users


@router.get("/{user_id}", response_model=UserModel)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserModel)
async def create_tag(body: UserModel, db: Session = Depends(get_db)):
    return await repository_users.create_user(body, db)


@router.put("/{user_id}", response_model=UserModel)
async def update_user(body: UserModel, user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=UserModel)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.remove_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/bdays/", response_model=List[UserModel])
async def read_bdays(db: Session = Depends(get_db)):
    users = await repository_users.get_users_bdays(db)
    return users