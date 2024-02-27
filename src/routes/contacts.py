from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactModel])
async def read_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user), name: str | None = None,
                     surname: str | None = None, email: str | None = None):
    users = await repository_contacts.get_contacts(skip, limit, current_user, db, name, surname, email)
    return users


@router.get("/{contact_id}", response_model=ContactModel)
async def read_user(contact_id: int, current_user: User = Depends(auth_service.get_current_user),
                    db: Session = Depends(get_db)):
    user = await repository_contacts.get_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return user


@router.post("/", response_model=ContactModel)
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactModel)
async def update_contact(body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    user = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return user


@router.delete("/{contact_id}", response_model=ContactModel)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    user = await repository_contacts.remove_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/bdays/", response_model=List[ContactModel])
async def read_bdays(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    users = await repository_contacts.get_contacts_bdays(current_user, db)
    return users
