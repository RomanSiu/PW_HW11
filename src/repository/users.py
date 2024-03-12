from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
        Retrieves a user with the specified email.

        :param email: The email of the user to retrieve.
        :type email: str
        :param db: The database session.
        :type db: Session
        :return: The user with the specified email, or None if it does not exist.
        :rtype: User | None
        """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
        Creates a new user.

        :param body: The data for the user to create.
        :type body: UserModel
        :param db: The database session.
        :type db: Session
        :return: The newly created user.
        :rtype: User
        """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
        Updates a token for a specific user.

        :param user: The user to update the token for.
        :type user: User
        :param token: The token to update.
        :type token: str
        :param db: The database session.
        :type db: Session
        :return: None.
        :rtype: None
        """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
        Change param of confirmation email for specific user.

        :param email: The email of the user to confirm.
        :type email: str
        :param db: The database session.
        :type db: Session
        :return: None.
        :rtype: None
        """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
        Updates an avatar for a specific user.

        :param email: Email of the specific user to update an avatar for.
        :type email: str
        :param url: The URL of the avatar.
        :type url: str
        :param db: The database session.
        :type db: Session
        :return: The updated user.
        :rtype: User
        """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
