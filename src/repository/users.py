from typing import List

from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from datetime import date, timedelta

from src.database.models import User
from src.schemas import UserModel


async def get_users(skip: int, limit: int, db: Session, name: str | None = None, surname: str | None = None,
                    email: str | None = None) -> List[User]:
    if name:
        return db.query(User).filter(User.name == name).all()
    if surname:
        return db.query(User).filter(User.surname == surname).all()
    if email:
        return db.query(User).filter(User.email == email).all()
    else:
        return db.query(User).offset(skip).limit(limit).all()


async def get_user(user_id: int, db: Session) -> User:
    return db.query(User).filter(User.id == user_id).first()


async def create_user(body: UserModel, db: Session) -> User:
    user = User(name=body.name, surname=body.surname, email=body.email, phone=body.phone, born_date=body.born_date)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(user_id: int, body: UserModel, db: Session) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = body.name
        user.surname = body.surname
        user.email = body.email
        user.phone = body.phone
        user.born_date = body.born_date
        db.commit()
    return user


async def remove_user(user_id: int, db: Session) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_users_bdays(db: Session) -> List[User]:
    dateFrom = date.today()
    dateTo = date.today() + timedelta(days=7)
    thisYear = dateFrom.year
    nextYear = dateFrom.year + 1
    return (db.query(User).filter(
        or_(
            func.to_date(func.concat(func.to_char(User.born_date, "DDMM"), thisYear), "DDMMYYYY").between(dateFrom,
                                                                                                        dateTo),
            func.to_date(func.concat(func.to_char(User.born_date, "DDMM"), nextYear), "DDMMYYYY").between(dateFrom,
                                                                                                        dateTo)))
            .all())
