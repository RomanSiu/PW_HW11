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
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :param name: The name of the contact to retrieve.
    :type name: str, optional
    :param surname: The surname of the contact to retrieve.
    :type surname: str, optional
    :param email: The email of the contact to retrieve.
    :type email: str, optional
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    users = await repository_contacts.get_contacts(skip, limit, current_user, db, name, surname, email)
    return users


@router.get("/{contact_id}", response_model=ContactModel)
async def read_user(contact_id: int, current_user: User = Depends(auth_service.get_current_user),
                    db: Session = Depends(get_db)):
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param current_user: The user to retrieve the contact for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    user = await repository_contacts.get_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return user


@router.post("/", response_model=ContactModel)
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param current_user: The user to create the note for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactModel)
async def update_contact(body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactModel
    :param current_user: The user to update the contact for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    user = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return user


@router.delete("/{contact_id}", response_model=ContactModel)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param current_user: The user to remove the contact for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    user = await repository_contacts.remove_contact(contact_id, current_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/bdays/", response_model=List[ContactModel])
async def read_bdays(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Retrieves a list of contacts for a specific user with birthday in next 7 days.

    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    users = await repository_contacts.get_contacts_bdays(current_user, db)
    return users
