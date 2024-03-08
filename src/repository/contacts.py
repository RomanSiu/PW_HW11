from typing import List

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from datetime import date, timedelta

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session, name: str = None, surname: str = None,
                       email: str = None) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param name: The name of the contact to retrieve.
    :type name: str, optional
    :param surname: The surname of the contact to retrieve.
    :type surname: str, optional
    :param email: The email of the contact to retrieve.
    :type email: str, optional
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    if name:
        return db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).all()
    if surname:
        return db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).all()
    if email:
        return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).all()
    else:
        return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user,id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    user = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, born_date=body.born_date,
                   user_id=user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactModel
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    user = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if user:
        user.name = body.name
        user.surname = body.surname
        user.email = body.email
        user.phone = body.phone
        user.born_date = body.born_date
        db.commit()
    return user


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    user = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_contacts_bdays(user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with birthday in next 7 days.

    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    dateFrom = date.today()
    dateTo = date.today() + timedelta(days=7)
    thisYear = dateFrom.year
    nextYear = dateFrom.year + 1
    return (db.query(Contact).filter(
        and_(or_(
            func.to_date(func.concat(func.to_char(Contact.born_date, "DDMM"), thisYear), "DDMMYYYY").between(dateFrom,
                                                                                                        dateTo),
            func.to_date(func.concat(func.to_char(Contact.born_date, "DDMM"), nextYear), "DDMMYYYY").between(dateFrom,
                                                                                                        dateTo)),
        Contact.user_id == user.id))
            .all())
